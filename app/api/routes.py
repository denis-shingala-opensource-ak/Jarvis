"""REST API endpoints."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.models.schemas import HealthResponse
from app.models import database as db
from app.utils.auth import user_dependency

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, user: user_dependency):
    """Serve the main dashboard page."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "app_name": settings.APP_NAME},
    )


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Serve the login page."""
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "app_name": settings.APP_NAME},
    )


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Serve the registration page."""
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "app_name": settings.APP_NAME},
    )


@router.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        llm_provider=settings.LLM_PROVIDER,
        stt_provider=settings.STT_PROVIDER,
        tts_provider=settings.TTS_PROVIDER,
    )


@router.get("/api/conversations")
def list_conversations():
    """List all conversation sessions."""
    return db.list_conversations()


@router.get("/api/conversations/{conversation_id}/messages")
def get_messages(conversation_id: str):
    """Get messages for a specific conversation."""
    return db.get_conversation_history(conversation_id)
