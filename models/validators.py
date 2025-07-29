from pydantic import BaseModel


class PostCharacter(BaseModel):
    character_id: int
    

class NewMessage(BaseModel):
    telegram_id: int
    message_text: str
    image: str | None


class InitData(BaseModel):
    initData: str


class CreateCharacter(BaseModel):
    avatar_img_url: str
    shape: dict
    name: str
    sex: str
    appearance: str
    archetypes: list[str]
    additionalDetails: str
    interests: list[str]
    abilities: list[str]
    places: list[str]
    

class OnlyUser(BaseModel):
    telegram_id: int