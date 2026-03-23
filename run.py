"""Jarvis Voice Assistant - Entry Point"""
import uvicorn
from dotenv import load_dotenv
from app.core.config import settings

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        env_file='./.env',
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
