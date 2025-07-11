# from fastapi.encoders import jsonable_encoder
# from pydantic import BaseModel
# from typing import Optional, List
# from .model import SexEnum


# class CharacterOut(BaseModel):
#     id: int
#     name: str
#     is_default: bool
#     avatar_url: str
#     sex: SexEnum
#     interests: List[str]
#     abilities: List[str]
#     places: List[str]
#     additional_details: Optional[str]
#     subtitle: Optional[str]

#     class Config:
#         from_attributes = True
        
    
# async def final_data_user(user_id: int, chosen_character, characters: list):
#     user_data = {
#         'user': {
#             'telegram_id': user_id,
#             'characters': jsonable_encoder([CharacterOut.from_orm(ch) for ch in characters]),
#             'chosen_character': None
#         },
#         'accessToken': None
#     }

#     if chosen_character:
#         try:
#             user_data['user']['chosen_character'] = jsonable_encoder(CharacterOut.from_orm(chosen_character))
#         except Exception:
#             pass

#     return user_data
    