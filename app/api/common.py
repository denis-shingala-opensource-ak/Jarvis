
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from fastapi.logger import logger
from fastapi.responses import HTMLResponse, RedirectResponse

from app.models.database import settings, engine
from fastapi.templating import Jinja2Templates
from app.utils.auth import user_dependency

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info(f"Starting {settings.APP_NAME}...")
    logger.info("Database initialized.")
    logger.info(f"LLM Provider: {settings.LLM_PROVIDER} ({settings.LLM_MODEL})")
    logger.info(f"STT Provider: {settings.STT_PROVIDER}")
    logger.info(f"TTS Provider: {settings.TTS_PROVIDER}")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}...")
    engine.dispose()

@router.get("/logout")
async def logout(request: Request):
    """Clear all cookies and redirect to login."""
    response = RedirectResponse(url="/login", status_code=302)
    for cookie_name in request.cookies:
        response.delete_cookie(cookie_name, path="/")
    return response

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

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, user: user_dependency):
    """Serve the main dashboard page."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "app_name": settings.APP_NAME},
    )