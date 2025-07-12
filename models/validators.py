from pydantic import BaseModel


class PostCharacter(BaseModel):
    character_id: int


class NewMessage(BaseModel):
    telegram_id: int
    message_text: str


class InitData(BaseModel):
    initData: str