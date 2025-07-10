from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .auth_conf import UserAuth
from .cookies import cookies
from db.character_parser import final_data_user
from db_requests.user import set_user, get_user, get_characters


router = APIRouter(prefix='/auth', tags=['Работа с авторизации'])


class InitData(BaseModel):
    initData: str
        

@router.post('/login')
async def login_user(data: InitData):
    auth = UserAuth()
    
    verify = await auth.telegram_validate(init_data=data.model_dump())
    user_id = verify['id']
    
    if verify['result']:
        response_db = await get_user(user_id)
        
        if response_db['code'] == 200:
            user = response_db['user']
            characters = await get_characters(user_id)
            
            final_data = await final_data_user(user_id=user_id, chosen_character=user.chosen, characters=characters)
            
            access_token = await auth.create_acess_token(user_id=user_id, expire_minutes=120)
            
            final_data['accessToken'] = access_token
            
            response = JSONResponse(content=final_data)
            # response = cookies(response=response) Чекни, что тут и если что, подправь(Бауэру)
            
            #  Я просто не понял. В итоге лучше с access сделать? Без http only refresh. Он нам по факту не нужен
            return response
        
        return JSONResponse(content=response_db['message'], status_code=response_db['code'])
    
    return JSONResponse(content={'response': 'access denied'})


@router.post('/register')
async def login_user(data: InitData):
    auth = UserAuth()
    
    verify = await auth.telegram_validate(init_data=data.model_dump())
    user_id = verify['id']
    
    if verify['result']:
        response_db = await set_user(user_id)
        
        if response_db['code'] == 201:
            user = response_db['user']
            characters = await get_characters(user_id)
            
            final_data = await final_data_user(user_id=user_id, chosen_character=user.chosen, characters=characters)
            
            access_token = await auth.create_acess_token(user_id=user_id, expire_minutes=120)
            
            final_data['accessToken'] = access_token

            response = JSONResponse(content=final_data)
            # response = cookies(response=response) Чекни, что тут и если что, подправь(Бауэру)
            #  Я просто не понял. В итоге лучше с access сделать? Без http only refresh. Он нам по факту не нужен

            
            return response
        
    return JSONResponse(content={'response': 'access denied'}, status_code=403)