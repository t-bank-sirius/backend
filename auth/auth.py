from fastapi import APIRouter
from pydantic import BaseModel

from .auth_conf import UserAuth

router = APIRouter(prefix='/auth', tags=['Работа с авторизации'])


class InitData(BaseModel):
    initData: str
        

@router.post('/login')
async def login_user(data: InitData):
    auth = UserAuth()
    
    verify = auth.telegram_validate(init_data=data.model_dump())
    
    if verify:
        return {'response': 'meow'}
    
    return {'response': 'nooo'}


@router.post('/register')
async def login_user(data: InitData):
    auth = UserAuth()
    
    verify = auth.telegram_validate(init_data=data.model_dump())
    
    if verify:
        return {'response': 'meow'}
    
    return {'response': 'nooo'}