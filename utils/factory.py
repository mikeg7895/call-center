from app.serivces.main_services import MainService
from app.serivces.auth_services import AuthService
from app.serivces.websocket_services import WebSocketService

class Factory:
    def get_main_service(self):
        return MainService()
    
    def get_auth_service(self):
        return AuthService()
    
    def get_websocket_service(self):
        return WebSocketService()