from urllib.parse import unquote
from datetime import timedelta, datetime
from pydantic_settings import BaseSettings, SettingsConfigDict

import json
import hmac
import hashlib
import jwt
    
    
class JWTSecret(BaseSettings):
    SECRET: str
    ALGORITHM: str
    
    model_config = SettingsConfigDict(env_prefix="JWT_")


class BotSecret(BaseSettings):
    TOKEN: str
    
    model_config = SettingsConfigDict(env_prefix="BOT_")
    
    
class UserAuth:
    
    def __init__(self):
        self.jwt_secret = JWTSecret()
        self.bot_secret = BotSecret()
        
    async def create_acess_token(self, user_id: int, expire_minutes: int = 15):
        expire = datetime.now() + timedelta(minutes=expire_minutes)
        
        payload = {
            "sub": str(user_id),
            "type": "access",
            "exp": expire
            }
        
        return jwt.encode(payload=payload, key=self.jwt_secret.SECRET, algorithm=self.jwt_secret.ALGORITHM)
            
    async def create_refresh_token(self, user_id: int, expire_days: int = 14):
        expire = datetime.now() + timedelta(minutes=expire_days)
        
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": expire
            }
        
        return jwt.encode(payload=payload, key=self.jwt_secret.SECRET, algorithm=self.jwt_secret.ALGORITHM)
    
    async def decode_token(self, token: str):
        try:
            token = jwt.decode(jwt=token, key=self.jwt_secret.SECRET, algorithms=self.jwt_secret.ALGORITHM)
        except jwt.ExpiredSignatureError:
            return "Токен истёк"
        except jwt.InvalidTokenError:
            return "Токен невалиден"
        
        return token

    async def telegram_validate(self, init_data: dict) -> dict | str:
        init_data = init_data['initData']
        
        vals = {k: unquote(v) for k, v in [s.split('=', 1) for s in init_data.split('&')]}
        user = json.loads(vals['user']) # Сам юзер
        user_id = user['id']
        
        data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(vals.items()) if k != 'hash')

        secret_key = hmac.new("WebAppData".encode(), self.bot_secret.TOKEN.encode(), hashlib.sha256).digest()
        
        h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)

        return {"result": h.hexdigest() == vals['hash'], 'id': user_id}