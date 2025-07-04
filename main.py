from fastapi import FastAPI
from auth.auth import router as auth_router
import uvicorn


app = FastAPI(
    title="Мой API",
    description="Описание API на русском",
    version="1.0.0",
    swagger_ui_parameters={"lang": "ru"}
)

app.include_router(auth_router)
# class RegistrtationForm(BaseModel):
#     username: str
#     password: str
#     phone: str
    

# class LoginForm(BaseModel):
#     username: str
#     password: str
    

# @app.post("/registration")
# async def reg(data: RegistrtationForm):
#     user = data.model_dump()
#     MEMORY[user['username']] = user
    
#     return {'response': 'success'}


# @app.post('/login')
# async def login(data: LoginForm):
#     pars = data.model_dump()
#     user = pars.get('username')
    
#     if MEMORY.get(user):
#         mem = MEMORY.get(user)
#         if mem['password'] == pars['password']:
#             return {'response': mem}
    
#     return {'response': 'Не верный логин или пароль'}
    
    
if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8080, host='0.0.0.0')