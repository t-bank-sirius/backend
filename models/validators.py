from fastapi.requests import Request
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
    interests: list[str]
    abilities: list[str]
    places: list[str]


class Characters(BaseModel):
    id: int
    user_id: int | None
    name: str
    is_generated: bool
    avatar_img_url: str
    system_prompt: str
    init_message: str
    subtitle: str
    
    class Config:
        from_attributes = True
        
    def set_avatar_url(self, request: Request):
        if self.avatar_img_url:
            self.avatar_img_url = str(request.url_for("uploads", path=self.avatar_img_url))
        