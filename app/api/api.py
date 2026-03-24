"""REST API endpoints."""

from fastapi import APIRouter, HTTPException
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.models.schemas import HealthResponse
from app.models import database as db

router = APIRouter(prefix="/api", tags=["api"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        llm_provider=settings.LLM_PROVIDER,
        stt_provider=settings.STT_PROVIDER,
        tts_provider=settings.TTS_PROVIDER,
    )

@router.get("/conversations")
def list_conversations():
    """List all conversation sessions."""
    return db.list_conversations()

@router.get("/conversations/{conversation_id}/messages")
def get_messages(conversation_id: str):
    """Get messages for a specific conversation."""
    return db.get_conversation_history(conversation_id)

@router.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: str):
    """Soft-delete a conversation."""
    deleted = db.delete_conversation(conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "deleted"}
