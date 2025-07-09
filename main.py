from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.auth import router as auth_router
import uvicorn


app = FastAPI(
    title="Мой API",
    description="Описание API на русском",
    version="1.0.0",
    swagger_ui_parameters={"lang": "ru"}
)

origins = [
    "https://pretty-keys-battle.loca.lt"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get('/')
async def index():
    return {'response': 'Hello, world'}
    

# if __name__ == '__main__':
#     uvicorn.run('main:app', reload=True, port=5000, host='0.0.0.0')