import uuid, chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.services.llm_service import BaseLLMService, OllamaLLMService

class VectorEmbeddings:
    def __init__(self):
        self._chromadb_client = chromadb.PersistentClient(path="./chroma")
        self._chromadb_collection = self._chromadb_client.get_or_create_collection(name="jarvis_vectors")
        self._embedding_client: BaseLLMService = OllamaLLMService()

    async def add(self, conversation_id: str, role: str, text: str, user_id: int):
        """ store the vectors in the chroma db """
        if not text or not text.strip():
            return
        
        text_splitters = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)
        chunks = text_splitters.split_text(text=text)

        for chunk in chunks:
            embeddings = await self._embedding_client.create_embeddings(chunk)

            # add into vector DB
            self._chromadb_collection.add(
                ids=[str(uuid.uuid4())],
                embeddings=[embeddings],
                documents=[text],
                metadatas=[{
                    "role": role,
                    "conversation_id": conversation_id,
                    "user_id": str(user_id)
                }]
            )

    async def similarity_search(self, text: str, user_id: int, conv_id: str, top_k: int = 5):
        """ search top-K simantically similar vector for this user """
        # check if there are any documents for this user first
        existing = self._chromadb_collection.get(
            where={"user_id": str(user_id)},
            limit=1
        )
        if not existing["ids"]:
            return []

        query = await self._embedding_client.create_embeddings(text)

        # similarity search
        result = self._chromadb_collection.query(
            query_embeddings=[query],
            n_results=top_k,
            where={
                "$and": [
                    {"conversation_id": conv_id},
                    {"user_id": str(user_id)}
                ]
            }
        )
        return result["documents"][0] if result["documents"] else []