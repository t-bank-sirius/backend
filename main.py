from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from auth.auth import router as auth_router
from user.user import router as user_router
import uvicorn

from dotenv import load_dotenv

import os


load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), override=True)


app = FastAPI(
    title="Мой API",
    description="Описание API Junior Assistant",
    version="1.0.0",
    swagger_ui_parameters={"lang": "ru"}
)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


origins = [
    "https://all-squids-film.loca.lt"
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


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8000, host='0.0.0.0')