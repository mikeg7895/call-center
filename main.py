from app.config import database
from app.models import base_model
from app.controllers import main_controller, auth_controller
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.middleware("http")
# async def auth_middleware(request: Request, call_next):
#     unprotected_routes = ["/login/", "/register/", "/", "/static/styles.css", "/static/script.js"]

#     if request.url.path not in unprotected_routes:
#         name_cookie = request.cookies.get("session_call")
#         if not name_cookie:
#             return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
        
#     response = await call_next(request)
#     return response


base_model.Base.metadata.create_all(bind=database.engine)

app.include_router(main_controller.router)
app.include_router(auth_controller.router)

