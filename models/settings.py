from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSecret(BaseSettings):
    SECRET: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    model_config = SettingsConfigDict(env_prefix="JWT_")


class BotSecret(BaseSettings):
    TOKEN: str
    
    model_config = SettingsConfigDict(env_prefix="BOT_")
    

class DatabaseSettings(BaseSettings):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    DB: str

    model_config = SettingsConfigDict(env_prefix='POSTGRES_')


class AppSettings(BaseSettings):
    FRONTEND_URL: str
    BOT_URL: str
    LLM_URL: str
    
    model_config = SettingsConfigDict(env_prefix='SERVICE_')