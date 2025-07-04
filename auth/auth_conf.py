from datetime import timedelta, datetime
from pydantic_settings import BaseSettings, SettingsConfigDict
import jwt


class JWTSecret(BaseSettings):
    SECRET: str
    ALGORITHM: str
    
    model_config = SettingsConfigDict(env_prefix="JWT_")

    
class UserAuth:
    
    def create_acess_token(self, user_id: int, expire_minutes: int = 15):
        jwt_secret = JWTSecret()
        expire = datetime.now() + timedelta(minutes=expire_minutes)
        
        payload = {
            "sub": user_id,
            "type": "access",
            "exp": expire
            }
        
        return jwt.encode(payload=payload, key=jwt_secret.SECRET, algorithm=jwt_secret.ALGORITHM)
            
    def create_refresh_token(self, user_id: int, expire_days: int = 14):
        jwt_secret = JWTSecret()
        expire = datetime.now() + timedelta(minutes=expire_days)
        
        payload = {
            "sub": user_id,
            "type": "refresh",
            "exp": expire
            }
        
        return jwt.encode(payload=payload, key=jwt_secret.SECRET, algorithm=jwt_secret.ALGORITHM)