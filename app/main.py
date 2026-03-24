"""FastAPI application factory."""

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api import api, auth, websocket
from app.api import common
from app.api.common import lifespan
from app.core.config import settings
from app.utils.auth import AuthRedirectException

app = FastAPI(
    title=settings.APP_NAME,
    description="Jarvis Smart Voice Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

@app.exception_handler(AuthRedirectException)
async def auth_redirect_handler(request: Request, exc: AuthRedirectException):
    return RedirectResponse(url="/login", status_code=302)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(api.router)
app.include_router(auth.router)
app.include_router(common.router)
app.include_router(websocket.router)
