from typing import Set

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "dndbot"
    LOG_LEVEL: str = "INFO"

    TOKEN: str = Field(alias="PLAYER_BOT_TOKEN")
    ADMIN_IDS: Set[int]

    BACKEND_URL: str = "http://backend:8000"

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DB: int = Field(alias="PLAYER_REDIS_DB")


settings = Settings()
