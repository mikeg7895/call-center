from app.utils.current_user import get_current_user
from app.utils.exceptions import TokenNotValid
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.exceptions import HTTPException
import json

class WebSocketService:
    def __init__(self):
        self.clients: dict = {}

    async def get_user(self, websocket: WebSocket):
        try: 
            token = websocket.query_params.get('token')
            token_data = await get_current_user(token)
            if not token_data:
                raise TokenNotValid("Token not valid")
            return token_data.name
        except HTTPException:
            await websocket.close()   
            raise TokenNotValid("Token not valid")

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        try:
            user = await self.get_user(websocket)
            self.clients[user] = websocket
            print(f"Cliente conectado. Total de clientes: {len(self.clients)}")
            while True:
                await websocket.receive_text()
        except (WebSocketDisconnect, TokenNotValid):
            await self.disconnect(websocket)

    async def disconnect(self, websocket: WebSocket):
        key = [k for k, v in self.clients.items() if v == websocket]
        if len(key) > 0:
            self.clients.pop(key[0])
            print(f"Cliente desconectado. Total de clientes: {len(self.clients)}")

    async def broadcast(self, message: dict, user: str):
        json_message = json.dumps(message)
        try: 
            await self.clients[user].send_text(json_message)
        except WebSocketDisconnect:
            self.disconnect(self.clients[user.position_queue])
