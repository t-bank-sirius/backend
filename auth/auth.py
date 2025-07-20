from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .auth_conf import UserAuth
from my_requests.db.user import set_user, get_user
from models.validators import InitData
from my_requests.db.user import get_db_session


router = APIRouter(prefix='/auth', tags=['Работа с авторизацией'])


@router.post('/login')
async def login_user(data: InitData, session: AsyncSession = Depends(get_db_session)):
    auth = UserAuth()
    
    user_id = await auth.telegram_validate(init_data=data.model_dump())
    await get_user(user_id=user_id, session=session)
    
    expire_minutes = auth.jwt_secret.ACCESS_TOKEN_EXPIRE_MINUTES
    access_token = await auth.create_acess_token(user_id=user_id, expire_minutes=expire_minutes)
              
    return JSONResponse(content={'accessToken': access_token})


@router.post('/register')
async def register_user(data: InitData, session: AsyncSession = Depends(get_db_session)):
    auth = UserAuth()
    
    user_id: int = await auth.telegram_validate(init_data=data.model_dump())
    await set_user(user_id, session=session)
     
    expire_minutes = auth.jwt_secret.ACCESS_TOKEN_EXPIRE_MINUTES
    access_token = await auth.create_acess_token(user_id=user_id, expire_minutes=expire_minutes)
    
    return JSONResponse(content={'accessToken': access_token})