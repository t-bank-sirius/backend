from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from auth.auth import router as auth_router
from user.user import router as user_router
from models.settings import AppSettings

from dotenv import load_dotenv

import os


load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), override=True)


app = FastAPI(
    title="Мой API",
    description="Описание API Junior Assistant",
    version="1.0.0",
    swagger_ui_parameters={"lang": "ru"}
)


origins = [
    'https://user541820783-z2uihaxm.tunnel.vk-apps.com'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(auth_router)
app.include_router(user_router)