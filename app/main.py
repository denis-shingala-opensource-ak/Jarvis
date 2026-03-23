"""FastAPI application factory."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import routes, websocket
from app.core.config import settings
from app.core.logging_config import logger
from app.models.database import engine


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


app = FastAPI(
    title=settings.APP_NAME,
    description="Jarvis Smart Voice Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(routes.router)
app.include_router(websocket.router)
