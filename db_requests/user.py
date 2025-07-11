import asyncio
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy import insert, select, or_
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
    except Exception as er:
            print(er)
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
            
    finally:
        await cfg.engine.dispose()


async def get_characters(user_id: int):
    cfg = Config()
    
    session = async_sessionmaker(cfg.engine)
    
    try:
        async with session() as session:
            query_characters = select(Character).where(
                    or_(
                        Character.user_id == user_id,
                        Character.is_default == True
                    )
                )
            response = await session.execute(query_characters)
            
            return response.scalars().all()
    finally:
        await cfg.engine.dispose()
    
    
async def set_character(
    user_id: int,
    name: str,
    is_default: bool,
    avatar_url: str,
    sex: str,
    interests: list[str],
    abilities: list[str],
    places: list[str],
    additional_details: str,
    subtitle: str
):
    cfg = Config()
    
    session = async_sessionmaker(cfg.engine)
    
    try:
        async with session() as session:
            query = insert(Character).values(
                user_id=user_id,
                name=name,
                is_default=is_default,
                avatar_url=avatar_url,
                sex=sex,
                interests=interests,
                abilities=abilities,
                places=places,
                additional_details=additional_details,
                subtitle=subtitle
                )
            
            await session.execute(query)
            await session.commit()
    finally:
        await cfg.engine.dispose()