"""WebSocket endpoint for real-time chat and voice communication."""
import json
import base64

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.chat_manager import ChatManager
from app.models.schemas import WebSocketMessage
from app.core.logging_config import logger
from app.utils.auth import ws_user_dependency

router = APIRouter()
chat_manager = ChatManager()

class ConnectionManager:
    """Manages active WebSocket connections."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")

    async def send_json(self, websocket: WebSocket, data: dict):
        await websocket.send_json(data)


manager = ConnectionManager()


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket, user: ws_user_dependency):
    await manager.connect(websocket)
    conversation_id = None

    if user is None:
        await websocket.close(code=1008, reason="Unauthorized")
        return

    try:
        while True:
            raw_data = await websocket.receive_text()
            msg = WebSocketMessage(**json.loads(raw_data))

            if msg.type == "text":
                # Send typing indicator
                await manager.send_json(websocket, {"type": "typing", "status": True})
                response = await chat_manager.chat_text(
                    text=msg.content,
                    conversation_id=msg.conversation_id or conversation_id,
                    tts_enabled=msg.tts_enabled,
                    user_id=user.user_id
                )

                conversation_id = response.conversation_id

                await manager.send_json(websocket, {"type": "typing", "status": False})
                await manager.send_json(
                    websocket,
                    {
                        "type": "text_response",
                        "message": response.message,
                        "conversation_id": response.conversation_id,
                        "audio_base64": response.audio_base64,
                        "timestamp": response.timestamp.isoformat(),
                    },
                )

            elif msg.type == "audio":
                # Send typing indicator
                await manager.send_json(
                    websocket, {"type": "typing", "status": True, "message": "Listening..."}
                )

                audio_bytes = base64.b64decode(msg.content)
                response = await chat_manager.chat_voice(
                    audio_bytes=audio_bytes,
                    conversation_id=msg.conversation_id or conversation_id,
                )
                conversation_id = response.conversation_id

                await manager.send_json(websocket, {"type": "typing", "status": False})
                await manager.send_json(
                    websocket,
                    {
                        "type": "voice_response",
                        "message": response.message,
                        "conversation_id": response.conversation_id,
                        "audio_base64": response.audio_base64,
                        "timestamp": response.timestamp.isoformat(),
                    },
                )

            elif msg.type == "control":
                if msg.content == "new_conversation":
                    if conversation_id:
                        chat_manager.clear_conversation(conversation_id)
                    conversation_id = None
                    await manager.send_json(
                        websocket,
                        {
                            "type": "control_response",
                            "message": "New conversation started",
                        },
                    )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await manager.send_json(
            websocket, {"type": "error", "message": str(e)}
        )
        manager.disconnect(websocket)
