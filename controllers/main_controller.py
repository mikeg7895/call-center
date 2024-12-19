from fastapi import APIRouter, File, UploadFile, HTTPException, WebSocket, Form, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Annotated
from app.services.main_services import MainService
from app.services.websocket_services import WebSocketService
from app.utils.json import to_dict

router = APIRouter()
ServiceMain = Annotated[MainService, Depends(MainService)]
ServiceWebSocket = Annotated[WebSocketService, Depends(WebSocketService)]


@router.get("/clients/")
def get_clients(main_service: ServiceMain):
    return {"data": main_service.get_clients()}


@router.delete("/clients/")
def delete_clients(main_service: ServiceMain):
    main_service.delete()
    return {"message": "Clients deleted"}


@router.post("/upload/")
async def load_xlsx(main_service: ServiceMain, file: UploadFile = File(...)):
    try:
        content = await file.read()
        clients = main_service.load_xlsx(content)
        return {"data": clients}
    except Exception as e:
        return {"error": str(e)}
    

@router.get("/export/")
def export_xlsx(main_service: ServiceMain):
    file = main_service.export_xlsx()
    return StreamingResponse(
        file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=clients.xlsx"}
    )
    

@router.get("/start-calls/")
def start_calls_method(main_service: ServiceMain, background_tasks: BackgroundTasks):
    status = main_service.validate_process()
    if "error" in status:
        raise HTTPException(status_code=400, detail=status["error"])
    background_tasks(main_service.start_calls())
    return {"message": "Calls started"}


@router.get("/stadistics/")
def get_stadistics(main_service: ServiceMain):
    return main_service.get_stadistics()


