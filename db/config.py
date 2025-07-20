from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from models.settings import DatabaseSettings


class Config:
    
    def __init__(self):
        self.settings = DatabaseSettings()
        self.engine: AsyncEngine = create_async_engine(self.async_url)
    
    @property
    def async_url(self):
        env = self.settings
        return f'postgresql+asyncpg://{env.USER}:{env.PASSWORD}@{env.HOST}:{env.PORT}/{env.DB}'


cfg = Config()
engine = create_async_engine(cfg.async_url, echo=True)
SessionMaker = async_sessionmaker(engine, expire_on_commit=False)