from app.schemes.auth_schema import Login, Register
from app.config.database import get_db
from app.models.base_model import Advisor
import bcrypt

class AuthService():
    def __init__(self):
        self.db = next(get_db())

    def login(self, login: Login):
        client = self.db.query(Advisor).filter(Advisor.name == login.name).first()
        if not client:
            return False
        is_correct = bcrypt.checkpw(login.password.encode("utf-8"), client.password)
        if not is_correct:
            return False
        client.active = True
        self.db.commit()
        return client
    
    def register(self, register: Register):
        try:
            encrypted_password = bcrypt.hashpw(register.password.encode("utf-8"), bcrypt.gensalt())
            advisor = Advisor(name=register.name, password=encrypted_password, phone_number=register.phone_number)
            self.db.add(advisor)
            self.db.commit()
            return True
        except Exception as e:
            return False
        
    def logout(self, name: str):
        client = self.db.query(Advisor).filter(Advisor.name == name).first()
        client.active = False
        self.db.commit()
        return True