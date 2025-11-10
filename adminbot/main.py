import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import handlers
from settings import settings


async def main() -> None:
    dp = Dispatcher()

    # сюда добавляются обработчики
    dp.include_routers(
        handlers.start_router,
    )

    bot = Bot(
        token=settings.TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
