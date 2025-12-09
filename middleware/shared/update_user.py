import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from utils.events import extract_user
from services.user import get_or_create_user

logger = logging.getLogger(__name__)


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]:
        tg_user = extract_user(event)

        if tg_user:
            user, created = await get_or_create_user(tg_user)
            if created:
                logger.info("New user created with id: %d and username %s", user.id, user.username)
            return await handler(event, {**data, "user": user})
        return await handler(event, data)
