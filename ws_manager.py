from fastapi import WebSocket
from schemas import Message


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[tuple[WebSocket, int]] = []

    async def connect(self, websocket: WebSocket, chat_id: int):
        await websocket.accept()
        self.active_connections.append((websocket, chat_id))

    def disconnect(self, websocket: WebSocket, chat_id: int):
        self.active_connections.remove((websocket, chat_id))

    async def send_message(self, message: Message, chat_id: int):
        for conn in self.active_connections:
            if conn[1] == chat_id:
                await conn[0].send_json(message.json())

