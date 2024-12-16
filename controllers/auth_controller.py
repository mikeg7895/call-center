from fastapi import APIRouter, Response, Cookie
from app.schemes.auth_schema import Login, Register
from app.utils.factory import Factory

router = APIRouter()
auth_service = Factory().get_auth_service()

@router.post("/login/")
def login(login: Login, response: Response):
    client = auth_service.login(login)
    if not client:
        return {"error": "Invalid credentials"}
    response.set_cookie(key="session_call", value=client.name)
    return {"message": "Success"}


@router.post("/register/")
def register(register: Register):
    is_registered = auth_service.register(register)
    if not is_registered:
        return {"error": "Error registering user"}
    return {"message": "Success"}


@router.post("/logout/")
def logout(response: Response, session_call: str = Cookie(None)):
    auth_service.logout(session_call)
    response.delete_cookie(key="session_call")
    return {"message": "Success"}