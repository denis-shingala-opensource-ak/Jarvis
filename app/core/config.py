"""Application configuration loaded from environment variables."""
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Literal

ENV_FILE = Path(__file__).resolve().parent.parent.parent / ".env"

class Settings(BaseSettings):

    # App
    APP_NAME: str = "Jarvis"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    SECRET_KEY: str = ""

    # LLM
    LLM_PROVIDER: Literal["openai", "anthropic", "gemini", "ollama"] = "ollama"
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    LLM_MODEL: str = ""
    LLM_HOST: str = ""
    LLM_MAX_TOKENS: int = 2048
    LLM_TEMPERATURE: float = 0.7
    SYSTEM_PROMPT: str = (
        "You are Jarvis, an intelligent and helpful voice assistant. "
        "Be concise, friendly, and precise. When responding to voice queries, "
        "keep answers brief unless asked for detail."
    )

    # Speech
    STT_PROVIDER: Literal["google_free", "openai_whisper"] = "google_free"
    TTS_PROVIDER: Literal["google_free", "openai_tts"] = "google_free"
    TTS_VOICE: str = "alloy"

    # Database
    DATABASE_URL: str = ""

    # Conversation
    MAX_CONVERSATION_HISTORY: int = 20

    # JWT
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"

    model_config = {
        "env_file": str(ENV_FILE),
        "env_file_encoding": "utf-8",
    }

settings = Settings()