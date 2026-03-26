"""LLM service with support for Google Gemini, OpenAI, and Anthropic Claude."""
from abc import ABC, abstractmethod
import token
from typing import AsyncGenerator

from ollama import AsyncClient

from app.core.config import settings
from app.core.exceptions import LLMServiceError, ConfigurationError
from app.core.logging_config import logger


class BaseLLMService(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def create_embeddings(self, text: str):
        pass

    @abstractmethod
    async def chat(self, messages: list[dict]) -> str:
        pass

    @abstractmethod
    def chat_stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        pass

class OllamaLLMService(BaseLLMService):
    def __init__(self):
        self.client = AsyncClient(host=settings.LLM_HOST)
        self.model = settings.LLM_MODEL

    async def create_embeddings(self, text: str):
        """ Generate the embedding with the help of ollama embedding model """
        vector_embeddings = await self.client.embed(model=settings.EMBEDDING_LLM_MODEL, input=text)
        return vector_embeddings.embeddings[0]

    async def chat(self, messages: list[dict]) -> str:
        try:
            response = await self.client.chat(
                model=self.model,
                messages=messages
            )
            content = response.message.content
            if not content:
                logger.warning(f"Ollama returned empty response for model {self.model}")
                return "I'm sorry, I couldn't generate a response. Please try again."
            return content
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            raise LLMServiceError(f"Ollama API error: {e}")

    async def chat_stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        try:
            stream = await self.client.chat(
                model=self.model,
                messages=messages,
                stream=True,
                format='json'
            )
            async for chunk in stream:
                if chunk.message.content:
                    yield chunk.message.content
        except Exception as e:
            logger.error(f"Ollama streaming error: {e}")
            raise LLMServiceError(f"Ollama streaming error: {e}")

def create_llm_service() -> BaseLLMService:
    """Factory function: returns the correct LLM service based on config."""
    if settings.LLM_PROVIDER == "ollama":
        return OllamaLLMService()
    else:
        raise ConfigurationError(f"Unknown LLM provider: {settings.LLM_PROVIDER}")
