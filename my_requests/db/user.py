from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import insert, select, or_, update
from db.model import User, Character
from typing import AsyncGenerator
from db.config import SessionMaker
from db.utils import db_errors_to_http


async def get_db_session() -> AsyncGenerator:
    async with SessionMaker() as session:
        yield session
        
        
@db_errors_to_http
async def set_user(user_id: int, session: AsyncSession):
    await session.execute(insert(User).values(id=user_id))
    await session.commit()
    
    result = await session.get(User, user_id)
    
    return {"user": result}
        

@db_errors_to_http
async def get_user(user_id: int, session: AsyncSession):
    user = await session.get(User, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return {'user': user}


@db_errors_to_http
async def get_characters(user_id: int, is_default: bool, session: AsyncSession) -> list | JSONResponse:
    if not is_default:   
        query_characters = select(Character).where(Character.is_generated == is_default)
    else:
        query_characters = select(Character).where(Character.user_id == user_id)
        
    response = await session.execute(query_characters)
    return response.scalars().all()
    

@db_errors_to_http
async def set_character(
    user_id: int,
    name: str,
    is_generated: bool,
    avatar_img_url: str,
    system_prompt: str,
    init_message: str,
    subtitle: str | None,
    session: AsyncSession
):
    query = insert(Character).values(
                user_id=user_id,
                name=name,
                is_generated=is_generated,
                avatar_img_url=avatar_img_url,
                system_prompt=system_prompt,
                init_message=init_message,
                subtitle=subtitle
                )
    await session.execute(query)
    await session.commit()
    

@db_errors_to_http
async def set_user_character(character_id: int, user_id: int, session: AsyncSession):
    query = update(User).filter(User.id == user_id).values(chosen_character=character_id)
    await session.execute(query)
    await session.commit()
            
    user = await get_user(user_id=user_id, session=session)
    return {'user': user}