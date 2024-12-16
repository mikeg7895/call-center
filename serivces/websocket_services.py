from app.config.database import get_db
from app.models.base_model import Advisor
from fastapi import WebSocket, WebSocketDisconnect
import json

class WebSocketService:
    def __init__(self):
        self.clients = []
        self.db = next(get_db())

    def get_user(self, websocket: WebSocket):
        user = websocket.query_params.get('user')
        return self.db.query(Advisor).filter_by(name=user).first()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        user = self.get_user(websocket)
        self.clients.append(websocket)
        user.position_queue = self.clients.index(websocket)
        self.db.commit()
        print(f"Cliente conectado. Total de clientes: {len(self.clients)}")
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            await self.disconnect(websocket)

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.clients:
            self.clients.remove(websocket)
            user = self.get_user(websocket)
            user.position_queue = None
            self.db.commit()
            print(f"Cliente desconectado. Total de clientes: {len(self.clients)}")

    async def broadcast(self, message: dict, user: str):
        json_message = json.dumps(message)
        user = self.db.query(Advisor).filter_by(name=user).first()
        try: 
            await self.clients[user.position_queue].send_text(json_message)
        except WebSocketDisconnect:
            self.disconnect(self.clients[user.position_queue])
