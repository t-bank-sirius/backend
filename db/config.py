from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


class DatabaseSettings(BaseSettings):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    DB: str

    model_config = SettingsConfigDict(env_prefix='POSTGRES_')


class Config:
    
    def __init__(self):
        self.settings = DatabaseSettings()
        self.engine: AsyncEngine = create_async_engine(self.async_url)
    
    @property
    def async_url(self):
        env = self.settings
        return f'postgresql+asyncpg://{env.USER}:{env.PASSWORD}@{env.HOST}:{env.PORT}/{env.DB}'