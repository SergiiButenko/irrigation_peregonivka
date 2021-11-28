from notification_service.schema.schema import WSMessage
from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from fastapi import status, Response
import json

router = APIRouter(
    prefix="/ws",
    tags=["web sockets"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(
            #     f"You wrote: {manager.active_connections}", websocket
            # )
            # await manager.broadcast(f"Client # says: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.post(
    "/broadcast",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def ws_send(message: WSMessage):
    return await manager.broadcast(json.dumps(message.dict()))
