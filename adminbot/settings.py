from typing import Set

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "dndadminbot"
    LOG_LEVEL: str = "INFO"

    TOKEN: str = Field(alias="ADMIN_BOT_TOKEN")
    ADMIN_IDS: Set[int]

    BACKEND_URL: str = "http://backend:8000"

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DB: int = Field(alias="ADMIN_REDIS_DB")


settings = Settings()
