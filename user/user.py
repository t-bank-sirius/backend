from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from auth.auth_conf import UserAuth
from my_requests.db.user import get_characters, set_user_character, get_user
from my_requests.servers.requests import say_hello, llm
from db.model import User, Character
from .validations import is_auth
from models.validators import NewMessage, PostCharacter, CreateCharacter, Characters


router = APIRouter(prefix='/user', tags=['Работа с пользователем'])
    
        
@router.get("/get-characters")
async def get_all_characters(request: Request, owns: bool = Query( ... )):
    chars = []
    auth = UserAuth()
    headers = request.headers
   
    is_authin = await is_auth(headers=headers, auth=auth)
    
    if isinstance(is_authin, JSONResponse):
        return is_authin
    
    characters = await get_characters(user_id=int(is_authin['sub']), is_default=owns)
    
    if isinstance(characters, JSONResponse):
        return characters
    
    for character in characters:
        char = Characters.from_orm(character)
        char.set_avatar_url(request=request)
        chars.append(char)
    
    return chars


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
    
    await say_hello(chat_id=user.id, init_message=character.init_message)
    
    return character


@router.post('/new-message')
async def new_message(data: NewMessage, request: Request):    
    user_id = data.telegram_id
    message = data.message_text
    image = data.image
    
    if image:
        print(f'image: {image[:20]}')
    print(f'Я получил user_id: {user_id} и message: {message}\n')
    
    user = await get_user(user_id=user_id)
    
    if user['code'] != 200:
        return JSONResponse(content=user, status_code=user['code'])

    character: Character = user['user'].chosen
    
    if character is None:
        return JSONResponse(content={'message': 'У вас нет выбраного персонажа'}, status_code=404)
    
    response_llm = await llm(
        message=message,
        user_id=str(user_id),
        role=character.name,
        system_prompt=character.system_prompt,
        image_base64=image
        )
    
    return response_llm


@router.post('/new-character')
async def create_new_character(data: CreateCharacter):
    ...