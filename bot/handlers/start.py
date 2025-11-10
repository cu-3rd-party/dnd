from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from filters.admin import AdminFilter

router = Router()


@router.message(CommandStart(), ~AdminFilter())
async def start_command(message: Message) -> None:
    await message.answer(text="Этот бот пока что ничего не делает")


@router.message(CommandStart(), AdminFilter())
async def start_command(message: Message) -> None:
    await message.answer(text="Привет, админ!")
