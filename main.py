from app.config import database
from app.models import base_model
from app.controllers import main_controller, auth_controller, sockets_controller
from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
base_model.Base.metadata.create_all(bind=database.engine)

@app.get("/", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(
    main_controller.router,
    dependencies=[Depends(oauth_scheme)],
    tags=["main"]
)

app.include_router(
    auth_controller.router,
    tags=["auth"]
)

app.include_router(
    sockets_controller.router,
    tags=["sockets"]
)
