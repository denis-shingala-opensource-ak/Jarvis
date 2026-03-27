"""Chat manager: orchestrates LLM calls with conversation context."""
import base64, uuid, fitz
from typing import AsyncGenerator, Optional
from datetime import datetime, timezone


from app.core.config import settings
from app.core.logging_config import logger
from app.services.vector_embeddings import VectorEmbeddings
from app.services.llm_service import create_llm_service, BaseLLMService
from app.services.speech_service import SpeechService
from app.models.schemas import ChatResponse, RequestFile
from app.models.database import get_conversation_history, get_conversations, save_message


class ChatManager:
    def __init__(self):
        self.llm: BaseLLMService = create_llm_service()
        self.speech: SpeechService = SpeechService()
        self.chromadb: VectorEmbeddings = VectorEmbeddings()

        # In-memory conversation cache: {conversation_id: [messages]}
        self._conversations: dict[str, list[dict]] = {}

    def _get_or_create_conversation(self, conversation_id: Optional[str] = None, user_id: str = None) -> str:
        """Return existing or create new conversation ID."""
        # If conversation already in memory, reuse it
        if conversation_id and conversation_id in self._conversations:
            return conversation_id

        # Load from DB
        db_conversations = get_conversations(user_id)
        self._conversations.update(db_conversations)

        if conversation_id and conversation_id in self._conversations:
            # Ensure system prompt exists for DB-loaded conversations
            messages = self._conversations[conversation_id]
            if not messages or messages[0].get("role") != "system":
                messages.insert(0, {"role": "system", "content": settings.SYSTEM_PROMPT})
            return conversation_id

        new_id = conversation_id or str(uuid.uuid4())
        self._conversations[new_id] = [
            {"role": "system", "content": settings.SYSTEM_PROMPT}
        ]
        return new_id

    def _extract_text(self, content: str, mime_type: str, filename: str) -> str:
        """Extract text content from file bytes based on type."""
        raw = base64.b64decode(content)

        if mime_type and mime_type == "application/pdf":
            text = ''
            with fitz.open(stream=raw, filetype="pdf") as doc:
                text: str = "\n".join(page.get_text() for page in doc)

            return text.strip()

        # For text-based files, try common encodings
        for encoding in ("utf-8", "latin-1", "cp1252"):
            try:
                return raw.decode(encoding).strip()
            except (UnicodeDecodeError, ValueError):
                continue

        logger.warning(f"Could not extract text from file: {filename}")
        return ""

    def _trim_history(self, conversation_id: str):
        """Keep conversation within MAX_CONVERSATION_HISTORY limit."""
        messages = self._conversations[conversation_id]
        if len(messages) > settings.MAX_CONVERSATION_HISTORY + 1:
            self._conversations[conversation_id] = (
                [messages[0]] + messages[-(settings.MAX_CONVERSATION_HISTORY):]
            )

    async def chat_text(
        self,
        text: str,
        conversation_id: Optional[str] = None,
        tts_enabled: bool = False,
        user_id: Optional[int] = None,
        files: Optional[list[RequestFile]] = None,
    ) -> AsyncGenerator[ChatResponse, None]:
        """Handle a text chat message."""
        conv_id = self._get_or_create_conversation(conversation_id, user_id)

        # Add user message to history
        self._conversations[conv_id].append({"role": "user", "content": text})

        for file in files or []:
            content = self._extract_text(file.content, file.type, file.name)
            if content:
                await self.chromadb.add(conv_id, "user", content, user_id)

        # search the similar content from the vectordb (Chroma DB)
        context = await self.chromadb.similarity_search(text, user_id, conv_id)
        context = "\n".join(context)

        if context:
            prompt = f"""
                You are a helpful AI assistant.

                Answer the user's question using the retrieved context only when it is relevant and useful.
                If the retrieved context is unrelated, ignore it.
                If the question depends on information that is not present in the context, say you do not have enough information instead of guessing.
                Do not fabricate details.

                User question:
                {text}

                Retrieved context:
                {context}

                Provide a clear, direct answer.
            """

            self._conversations[conv_id].insert(0, {
                "role": "user",
                "content": prompt
            })

        # Call LLM
        response_text = ""
        async for response in self.llm.chat_stream(self._conversations[conv_id]):
            response_text += response
            yield ChatResponse(
                message=response,
                conversation_id=conv_id,
                timestamp=datetime.now(timezone.utc),
            )

        # Add assistant response to history
        self._conversations[conv_id].append(
            {"role": "assistant", "content": response_text}
        )
        self._trim_history(conv_id)

        # Persist to DB
        save_message(conv_id, "user", text, user_id=user_id)
        save_message(conv_id, "assistant", response_text, user_id=user_id)

        # store in vector DB
        await self.chromadb.add(conv_id, "user", text, user_id)
        await self.chromadb.add(conv_id, "assistant", response_text, user_id)

        # Optionally generate TTS
        audio_b64 = None
        if tts_enabled:
            audio_b64 = await self.speech.synthesize_base64(response_text)

        yield ChatResponse(
            message=response_text,
            conversation_id=conv_id,
            audio_base64=audio_b64,
            timestamp=datetime.now(timezone.utc),
            final_response=True
        )

    async def chat_voice(
        self,
        audio_bytes: bytes,
        conversation_id: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> ChatResponse:
        """Handle a voice message: STT -> LLM -> TTS."""
        # Transcribe audio to text
        transcribed_text = await self.speech.transcribe(audio_bytes)
        logger.info(f"Transcribed: {transcribed_text}")

        # Chat with LLM (with TTS enabled for voice responses)
        return await self.chat_text(
            text=transcribed_text,
            conversation_id=conversation_id,
            tts_enabled=True,
            user_id=user_id,
        )

    async def get_history(self, conversation_id: str) -> list[dict]:
        """Return conversation history from DB."""
        return await get_conversation_history(conversation_id)

    def clear_conversation(self, conversation_id: str):
        """Remove a conversation from in-memory cache."""
        self._conversations.pop(conversation_id, None)
