"""Request/response schemas and data models."""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime, timezone

class UserSchema(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    email: str
    password: str

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))
    is_voice: bool = False


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    audio_base64: Optional[str] = None
    timestamp: datetime


class ConversationSummary(BaseModel):
    conversation_id: str
    title: str
    message_count: int
    created_at: datetime
    updated_at: datetime


class HealthResponse(BaseModel):
    status: str
    version: str
    llm_provider: str
    stt_provider: str
    tts_provider: str


class WebSocketMessage(BaseModel):
    type: Literal["text", "audio", "control"]
    content: Optional[str] = None
    conversation_id: Optional[str] = None
    tts_enabled: bool = True


class JWTToken(BaseModel):
    email: str
    user_id: int
    exp: float