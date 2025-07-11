from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel
from auth.auth_conf import UserAuth
from db_requests.user import get_characters
from .validations import is_auth


router = APIRouter(prefix='/user', tags=['Работа с пользователем'])


class CharacterOut(BaseModel):
    id: str
    avatar_img_url: str
    name: str
    system_prompt: str
    init_message: str
    is_generated: bool

    class Config:
        from_attributes = True


class PostCharacter(BaseModel):
    character_id: int
    
        
@router.get("/get-characters", response_model=List[CharacterOut])
async def get_all_characters(request: Request):
    """
    Функция возвращает как всех default персонажей, так и персонажей которые сгенерировал пользователь (Если такие есть)
    """
    auth = UserAuth()
    headers = request.headers
    
    is_authin = await is_auth(headers=headers, auth=auth)

    if isinstance(is_authin, JSONResponse):
        return is_authin
    
    characters = await get_characters(user_id=int(is_authin['sub']))
    
    return characters


@router.post('/choose-character', response_model=List[CharacterOut])
async def choose_character(data: PostCharacter, request: Request):
    character_id = data.character_id
    
    auth = UserAuth()
    headers = request.headers
    
    is_authin = await is_auth(headers=headers, auth=auth)

    if isinstance(is_authin, JSONResponse):
        return is_authin
    
    