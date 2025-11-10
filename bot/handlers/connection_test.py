import requests
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from settings import settings

router = Router()


@router.message(Command("dbg_test_backend_connection"))
async def connection_test(message: Message) -> None:
    url = f"{settings.BACKEND_URL}/api/ping/"
    try:
        response: requests.Response = requests.get(url=url)
        assert isinstance(response, requests.Response), f"server returned {type(response)} instead of Response"
    except Exception as e:
        await message.answer(text=(
            "Внутренняя ошибка при попытке соединения с бэкендом:\n"
            f"{e}"
        ))
        return
    await message.answer(text=(
        f"Проверка соединения с бэкендом.\n"
        f"URL: {url}\n"
        f"StatusCode: {response.status_code}"
    ))
