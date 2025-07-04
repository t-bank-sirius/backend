from pydantic_settings import BaseSettings, SettingsConfigDict


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
    
    @property
    def async_url(self):
        env = self.settings
        return f'postgresql+asyncpg://{env.USER}:{env.PASSWORD}@{env.HOST}:{env.PORT}/{env.DB}'