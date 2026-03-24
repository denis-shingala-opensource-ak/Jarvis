"""Chat manager: orchestrates LLM calls with conversation context."""
import uuid
from typing import Optional
from datetime import datetime, timezone

from app.core.config import settings
from app.core.logging_config import logger
from app.services.llm_service import create_llm_service, BaseLLMService
from app.services.speech_service import SpeechService
from app.models.schemas import ChatResponse
from app.models.database import get_conversation_history, get_conversations, save_message


class ChatManager:
    def __init__(self):
        self.llm: BaseLLMService = create_llm_service()
        self.speech: SpeechService = SpeechService()
        # In-memory conversation cache: {conversation_id: [messages]}
        self._conversations: dict[str, list[dict]] = {}

    def _get_or_create_conversation(self, conversation_id: Optional[str] = None, user_id: str = None) -> str:
        """Return existing or create new conversation ID."""
        self._conversations = get_conversations(user_id)
        
        if conversation_id and conversation_id in self._conversations:
            return conversation_id
        new_id = conversation_id or str(uuid.uuid4())
        self._conversations[new_id] = [
            {"role": "system", "content": settings.SYSTEM_PROMPT}
        ]
        return new_id

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
    ) -> ChatResponse:
        """Handle a text chat message."""
        conv_id = self._get_or_create_conversation(conversation_id, user_id)

        # Add user message to history
        self._conversations[conv_id].append({"role": "user", "content": text})

        # Call LLM
        response_text = await self.llm.chat(self._conversations[conv_id])

        # Add assistant response to history
        self._conversations[conv_id].append(
            {"role": "assistant", "content": response_text}
        )
        self._trim_history(conv_id)

        # Persist to DB
        save_message(conv_id, "user", text, user_id=user_id)
        save_message(conv_id, "assistant", response_text, user_id=user_id)

        # Optionally generate TTS
        audio_b64 = None
        if tts_enabled:
            audio_b64 = await self.speech.synthesize_base64(response_text)

        return ChatResponse(
            message=response_text,
            conversation_id=conv_id,
            audio_base64=audio_b64,
            timestamp=datetime.now(timezone.utc),
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
