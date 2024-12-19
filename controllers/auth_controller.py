from typing import Annotated
from fastapi import APIRouter, Depends, Cookie, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.schemes.auth_schema import Register, Token
from app.services.auth_services import AuthService
from datetime import timedelta

router = APIRouter()
ServiceAuth = Annotated[AuthService, Depends(AuthService)]

@router.post("/login/")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response, auth_service: ServiceAuth):
    client = auth_service.login(form_data)
    if not client:
        return {"error": "Invalid credentials"}
    response.set_cookie(key="session_call", value=client.access_token)
    return {"message": "Success", "token": Token(access_token=client.access_token, token_type="bearer")}


@router.post("/register/")
def register(register: Register, auth_service: ServiceAuth):
    is_registered = auth_service.register(register)
    if not is_registered:
        return {"error": "Error registering user"}
    return {"message": "Success"}


@router.post("/logout/")
async def logout(response: Response, auth_service: ServiceAuth, session_call: str = Cookie(None)):
    await auth_service.logout(session_call)
    response.delete_cookie(key="session_call")
    return {"message": "Success"}