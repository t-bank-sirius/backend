from fastapi import APIRouter, Request, Query, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from my_requests.db.user import get_characters, set_user_character, get_user, set_character
from my_requests.servers.requests import say_hello, llm, generate_image, create_character, clear_context, add_face
from db.model import User, Character
from .validations import is_auth, is_auth_headers
from .utils import decode_and_save
from models.validators import NewMessage, PostCharacter, CreateCharacter, OnlyUser
from my_requests.db.user import get_db_session
from models.settings import ServerUrl


router = APIRouter(prefix='/user', tags=['Работа с пользователем'])
    
        
@router.get("/get-characters")
async def get_all_characters(owns: bool = Query( ... ), session: AsyncSession = Depends(get_db_session), auth = Depends(is_auth)):
    characters = await get_characters(user_id=int(auth['sub']), is_default=owns, session=session)
    return characters


@router.post('/choose-character')
async def choose_character(data: PostCharacter, session: AsyncSession = Depends(get_db_session), auth = Depends(is_auth)):
    character_id = data.character_id
    set_char_user = await set_user_character(character_id=character_id, user_id=int(auth['sub']), session=session)
    
    user: User = set_char_user['user']['user']
    character: Character = user.chosen
    
    await say_hello(chat_id=user.id, init_message=character.init_message)
    
    return character


@router.post('/new-message')
async def new_message(data: NewMessage, session: AsyncSession = Depends(get_db_session), auth = Depends(is_auth_headers)):
    user_id = data.telegram_id
    message = data.message_text
    image = data.image
    
    user = await get_user(user_id=user_id, session=session)

    character: Character = user['user'].chosen
    
    if character is None:
        raise HTTPException(detail='У вас нет выбраного персонаж', status_code=404)
    
    response_llm = await llm(
        message=message,
        user_id=str(user_id),
        role=character.name,
        system_prompt=character.system_prompt,
        image_base64=image
        )
    
    return response_llm


@router.post('/new-character')
async def create_new_character(data: CreateCharacter, request: Request, session: AsyncSession = Depends(get_db_session), auth = Depends(is_auth)):
    dump = data.model_dump()
    server = ServerUrl()
    user_id = int(auth['sub'])
    role = dump['name']
    
    await add_face(user_id=user_id, name=role, image=dump['avatar_img_url'])
    
    filename = await decode_and_save(dump['avatar_img_url'])
    url = request.app.url_path_for("avatars", path=filename)
    full_url = server.SERVER_URL.rstrip("/") + url

    dump['avatar_img_url'] = full_url
    
    char = await create_character(dump)
        
    data = {
        'user_id': user_id,
        'name': role,
        'is_generated': True,
        'avatar_img_url': full_url,
        'system_prompt': char['system_prompt'],
        'init_message': char['init_message'],
        'subtitle': char['subtitle']
    }
    await set_character(
        **data,
        session=session
    )
    
    return JSONResponse(content=data)
    

@router.post('/create-avatar')
async def create_avat(data: CreateCharacter, request: Request, auth = Depends(is_auth)):
    image = await generate_image(data=data.model_dump())
    
    return image


@router.post('/clear-context')
async def create_avat(data: OnlyUser, session: AsyncSession = Depends(get_db_session), auth = Depends(is_auth_headers)):
    user = await get_user(user_id=data.telegram_id, session=session)
    character: Character = user['user'].chosen
    
    if character is None:
        raise HTTPException(detail='У вас нет выбраного персонаж', status_code=404)
    
    message = await clear_context(user_id=data.telegram_id, role=character.name)
    
    return message