# settings.py
# from pathlib import Path
from pydantic import ConfigDict, model_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_URL: str = ""

    @model_validator(mode="after")
    def get_database_url(self):
        self.DB_URL = (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        return self

    model_config = ConfigDict(env_file=".env")


settings = Settings()
