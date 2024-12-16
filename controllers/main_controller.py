from fastapi import APIRouter, File, UploadFile, HTTPException, WebSocket, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.requests import Request
from app.utils.factory import Factory
from app.utils.json import to_dict

router = APIRouter()
templates = Jinja2Templates(directory="templates")
main_service = Factory().get_main_service()
websocket_service = Factory().get_websocket_service()

@router.get("/", response_class=HTMLResponse)
def main(request: Request):
    main_service.export_xlsx()
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/clients/")
def get_clients():
    return {"data": main_service.get_clients()}


@router.delete("/clients/")
def delete_clients():
    main_service.delete()
    return {"message": "Clients deleted"}


@router.post("/upload/")
async def load_xlsx(file: UploadFile = File(...)):
    try:
        content = await file.read()
        clients = main_service.load_xlsx(content)
        return {"data": clients}
    except Exception as e:
        return {"error": str(e)}
    

@router.get("/export/")
def export_xlsx():
    file = main_service.export_xlsx()
    return StreamingResponse(
        file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=clients.xlsx"}
    )
    

@router.get("/start-calls/")
def start_calls_method():
    status = main_service.start_calls()
    if "error" in status:
        raise HTTPException(status_code=400, detail=status["error"])
    return {"message": "Calls started"}


@router.post("/call-finished/")
async def call_finished(CallSid: str = Form(...), CallStatus: str = Form(...)):
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


@router.get("/stadistics/")
def get_stadistics():
    return main_service.get_stadistics()


@router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_service.connect(websocket)