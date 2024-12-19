from fastapi import APIRouter, Form, WebSocket, Depends
from app.services.main_services import MainService
from app.services.websocket_services import WebSocketService
from typing import Annotated

router = APIRouter()

ServiceMain = Annotated[MainService, Depends(MainService)]
ServiceWebSocket = Annotated[WebSocketService, Depends(WebSocketService)]


@router.post("/call-finished/")
async def call_finished(main_service: ServiceMain, websocket_service: ServiceWebSocket, CallSid: str = Form(...), CallStatus: str = Form(...)):
    if CallStatus != "in-progress":
        main_service.call_finished(CallSid, CallStatus)
        _, advisor = main_service.get_client_by_ssid(CallSid)
        await websocket_service.broadcast({"finished": True}, advisor.name)
    else:
        client, advisor = main_service.get_client_by_ssid(CallSid)
        data = {
            "client": client,
            "call_incoming": True
        }
        await websocket_service.broadcast(data, advisor.name)
    return {"message": "Call finished"}


@router.websocket("/ws/")
async def websocket_endpoint(websocket_service: ServiceWebSocket, websocket: WebSocket):
    await websocket_service.connect(websocket)