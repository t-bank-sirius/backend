from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional, List
from .model import SexEnum


class CharacterOut(BaseModel):
    id: int
    name: str
    is_default: bool
    avatar_url: str
    sex: SexEnum
    interests: List[str]
    abilities: List[str]
    places: List[str]
    additional_details: Optional[str]
    subtitle: Optional[str]

    class Config:
        from_attributes = True
        
    
async def final_data_user(user_id: int, chosen_character, characters: list):
    user_data = {
        'user': {
            'telegram_id': user_id,
            'characters': None,
            'chosen_character': None
        },
        'accessToken': None
    }
    chars = []
    
    for character in characters:
        to_dump = character[0]
        chars.append(CharacterOut.from_orm(to_dump))
    
    try:
        jsonbl_character = jsonable_encoder(CharacterOut.from_orm(chosen_character))
        user_data['user']['chosen_character'] = jsonbl_character
    except Exception:
        ...
    
    jsonbl = jsonable_encoder(chars)
    user_data['user']['characters'] = jsonbl
    
    return user_data
    