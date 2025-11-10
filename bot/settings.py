from typing import Set

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "dndbot"
    LOG_LEVEL: str = "INFO"

    BOT_TOKEN: str
    ADMIN_IDS: Set[int]

    BACKEND_URL: str = "http://backend:8000"

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DB: int


settings = Settings()
