from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .auth_conf import UserAuth
from my_requests.db.user import set_user, get_user
from models.validators import InitData


router = APIRouter(prefix='/auth', tags=['Работа с авторизацией'])


@router.post('/login')
async def login_user(data: InitData):
    auth = UserAuth()
    
    verify = await auth.telegram_validate(init_data=data.model_dump())
    user_id = verify['id']
    
    if verify['result']:
        response_db = await get_user(user_id)
        
        if response_db['code'] == 200:    
            access_token = await auth.create_acess_token(user_id=user_id, expire_minutes=auth.jwt_secret.ACCESS_TOKEN_EXPIRE_MINUTES)            
            return JSONResponse(content={'accessToken': access_token})
        
        return JSONResponse(content=response_db['message'], status_code=response_db['code'])
    
    return JSONResponse(content={'response': 'access denied'})


@router.post('/register')
async def register_user(data: InitData):
    auth = UserAuth()
    
    verify = await auth.telegram_validate(init_data=data.model_dump())
    user_id = verify['id']
    
    if verify['result']:
        response_db = await set_user(user_id)
        
        if response_db['code'] == 201:            
            access_token = await auth.create_acess_token(user_id=user_id, expire_minutes=auth.jwt_secret.ACCESS_TOKEN_EXPIRE_MINUTES)
            return JSONResponse(content={'accessToken': access_token})
        
        return JSONResponse(content={'response': response_db['message']})
        
    return JSONResponse(content={'response': 'access denied'}, status_code=403)