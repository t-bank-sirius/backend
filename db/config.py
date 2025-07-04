from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import create_engine
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    model_config = SettingsConfigDict(env_prefix='POSTGRES_')


class Config:
    
    def __init__(self):
        self.settings = DatabaseSettings()
    
    @property
    def async_url(self):
        env = self.settings
        return f'postgresql+asyncpg://{env.USERNAME}:{env.PASSWORD}@{env.HOST}:{env.PORT}/{env.DB_NAME}'