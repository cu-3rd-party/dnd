from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from httpx import AsyncClient

from settings import settings


class RegisterMiddleware(BaseMiddleware):
    def __init__(self, timeout=30.0):
        self.client = AsyncClient(timeout=timeout)

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        await self.client.post(
            settings.BACKEND_URL + "/api/player/register/",
            json={"telegram_id": event.from_user.id},
        )
        return await handler(event, data)
