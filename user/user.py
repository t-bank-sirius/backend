from aiohttp import ClientSession

from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel
from auth.auth_conf import UserAuth
from db_requests.user import get_characters, set_user_character
from db.model import User, Character
from .validations import is_auth


router = APIRouter(prefix='/user', tags=['Работа с пользователем'])


class PostCharacter(BaseModel):
    character_id: int
    
        
@router.get("/get-characters")
async def get_all_characters(request: Request, owns: bool = Query( ... )):
    """
    Функция возвращает как всех default персонажей, так и персонажей которые сгенерировал пользователь (Если такие есть)
    """
    auth = UserAuth()
    headers = request.headers
    
    is_authin = await is_auth(headers=headers, auth=auth)
    
    if isinstance(is_authin, JSONResponse):
        return is_authin
    
    characters = await get_characters(user_id=int(is_authin['sub']), is_default=owns)
    
    if isinstance(characters, JSONResponse):
        return characters
    
    return characters


@router.post('/choose-character')
async def choose_character(data: PostCharacter, request: Request):
    character_id = data.character_id
    
    auth = UserAuth()
    headers = request.headers
    
    is_authin = await is_auth(headers=headers, auth=auth)

    if isinstance(is_authin, JSONResponse):
        return is_authin
    
    set_char_user = await set_user_character(character_id=character_id, user_id=int(is_authin['sub']))
    
    if isinstance(set_char_user, JSONResponse):
        return set_char_user
    
    user: User = set_char_user['user']['user']
    character: Character = user.chosen
    
    data_to_bot = {
        'chat_id': user.id,
        'init_message': character.init_message
    }
    
    async with ClientSession() as session:
        async with session.post('http://127.0.0.1:5000/hello', json=data_to_bot) as response:
            print(response.status)
    
    return character
