from aiogram.filters import BaseFilter
from aiogram.types import Message

from settings import settings


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, **kwargs) -> bool:
        return message.from_user.id in settings.ADMIN_IDS
