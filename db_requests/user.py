import asyncio
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy import insert, select, or_, update
from db.config import Config
from db.model import User, Character


async def set_user(user_id: int):
    cfg = Config()
    
    session = async_sessionmaker(cfg.engine)
    
    try:
        async with session() as session:
            query = insert(User).values(id=user_id)
            await session.execute(query)
            await session.commit()
            
            new_user = await get_user(user_id)
            
            return {'user': new_user['user'], 'code': 201}
    except Exception:
            return {'message': 'Такой пользователь уже существует или вы ввели не корректные данные', 'code': 409}
    finally:
        await cfg.engine.dispose()
    
    
async def get_user(user_id: int):
    cfg = Config()
    
    session = async_sessionmaker(cfg.engine)
    
    try:
        async with session() as session:
            user: User = await session.get(User, user_id)
            
            if user:
                return {'user': user, 'code': 200}
            
            return {'message': 'Пользователя не существует', 'code': 404}
    except Exception:
        ... 
    finally:
        await cfg.engine.dispose()


async def get_characters(user_id: int, is_default: bool) -> list | JSONResponse:
    cfg = Config()
    
    session = async_sessionmaker(cfg.engine)
    
    try:
        async with session() as session:
            query_characters = select(Character).where(
                    or_(
                        Character.user_id == user_id,
                        Character.is_generated == is_default
                    )
                )
            response = await session.execute(query_characters)
            
            return response.scalars().all()
    except Exception:
        ...
    finally:
        await cfg.engine.dispose()
    
    return JSONResponse({'message': 'Вы передали не корректный user_id'}, 404)
    
    
async def set_character(
    user_id: int,
    name: str,
    is_generated: bool,
    avatar_img_url: str,
    system_prompt: str,
    init_message: str,
    subtitle: str | None
):
    cfg = Config()
    
    session = async_sessionmaker(cfg.engine)
    
    try:
        async with session() as session:
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
    finally:
        await cfg.engine.dispose()
        

async def set_user_character(character_id: int, user_id: int):
    cfg = Config()
    
    session = async_sessionmaker(cfg.engine)
    
    try:
        async with session() as session:
            query = update(User).filter(User.id == user_id).values(chosen_character=character_id)
            await session.execute(query)
            await session.commit()
            
            user = await get_user(user_id=user_id)
            
            return {'user': user, 'code': 200}
    except Exception:
        return JSONResponse({'message': 'Такого персонажа не существует'}, 404)
    finally:
        await cfg.engine.dispose()
