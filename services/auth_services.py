from app.schemes.auth_schema import Login, Register, Token
from app.config.database import get_db
from app.models.base_model import Advisor
from app.config.auth import create_access_token
from app.utils.current_user import get_current_user
from datetime import timedelta
import bcrypt

class AuthService():
    def __init__(self):
        self.db = next(get_db())

    def login(self, login):
        client = self.db.query(Advisor).filter(Advisor.name == login.username).first()
        if not client:
            return False
        is_correct = bcrypt.checkpw(login.password.encode("utf-8"), client.password)
        if not is_correct:
            return False
        access_token_expires = timedelta(minutes=30)
        acceess_token = create_access_token(
            data = {
                "sub": client.name,
            },
            expires_delta = access_token_expires
        )
        client.active = True
        self.db.commit()
        return Token(access_token=acceess_token, token_type="bearer")
    
    def register(self, register: Register):
        try:
            encrypted_password = bcrypt.hashpw(register.password.encode("utf-8"), bcrypt.gensalt())
            advisor = Advisor(name=register.name, password=encrypted_password, phone_number=register.phone_number)
            self.db.add(advisor)
            self.db.commit()
            return True
        except Exception as e:
            return False
        
    async def logout(self, cookie: str):
        token = await get_current_user(cookie)
        client = self.db.query(Advisor).filter(Advisor.name == token.name).first()
        client.active = False
        self.db.commit()
        return True