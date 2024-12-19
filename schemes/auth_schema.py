from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    name: str

class Login(BaseModel):
    name: str
    password: str
    ip: str


class Register(BaseModel):
    name: str
    password: str
    phone_number: str