from pydantic import BaseModel

class Login(BaseModel):
    name: str
    password: str
    ip: str


class Register(BaseModel):
    name: str
    password: str
    phone_number: str