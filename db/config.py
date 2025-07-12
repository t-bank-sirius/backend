from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from models.settings import DatabaseSettings


class Config:
    
    def __init__(self):
        self.settings = DatabaseSettings()
        self.engine: AsyncEngine = create_async_engine(self.async_url)
    
    @property
    def async_url(self):
        env = self.settings
        return f'postgresql+asyncpg://{env.USER}:{env.PASSWORD}@{env.HOST}:{env.PORT}/{env.DB}'