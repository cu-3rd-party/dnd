import base64
import io
import logging

from PIL import Image
from aiofiles import tempfile
from aiogram import Router, Bot
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Cancel, Row
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format
from httpx import AsyncClient

from settings import settings
from states.create_campaign import CreateCampaignStates
from states.mainmenu import MainMenuStates

router = Router()
logger = logging.getLogger(__name__)


async def on_name_entered(
    message: Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    text: str,
):
    dialog_manager.dialog_data["name"] = text
    await dialog_manager.next()


async def on_description_entered(
    message: Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    text: str,
):
    dialog_manager.dialog_data["description"] = text
    await dialog_manager.next()


async def on_icon_entered(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
):
    dialog_manager.dialog_data["icon"] = message.photo[-1].file_id

    await dialog_manager.next()


async def on_skip_description(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data["description"] = ""
    await dialog_manager.next()


async def on_skip_icon(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data["icon"] = None
    await dialog_manager.next()


async def get_icon(bot: Bot, file_id: str | None):
    if not file_id:
        return ""
    file = await bot.get_file(file_id)
    temp_input = await tempfile.NamedTemporaryFile(suffix=".raw")
    await bot.download_file(file.file_path, temp_input.name)
    with open(temp_input.name, "rb") as f:
        img = Image.open(f)
        output = io.BytesIO()
        img.save(output, format="PNG")
        return base64.b64encode(output.getvalue()).decode()


async def on_confirm(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    async with AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{settings.BACKEND_URL}/api/campaign/create/",
            json={
                "telegram_id": callback.from_user.id,
                "title": dialog_manager.dialog_data.get("name", ""),
                "icon": await get_icon(
                    callback.bot, dialog_manager.dialog_data.get("icon", "")
                ),
                "description": dialog_manager.dialog_data.get(
                    "description", "не указано"
                ),
            },
        )

        logger.debug(
            f"Sent request to create campaign for use {callback.from_user.id} and got status code {response.status_code}"
        )
        if response.status_code != 201:
            logger.error(
                f"Failed to create campaign for user {callback.from_user.id}: {response.status_code}"
            )
            await callback.answer(
                "Кампания не была создана успешно, попробуйте еще раз",
                show_alert=True,
            )
            return

        await callback.answer("Кампания создана успешно")
        await dialog_manager.start(MainMenuStates.main)


async def on_cancel(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await callback.message.answer("Создание кампании отменено")
    await dialog_manager.start(MainMenuStates.main)


async def get_confirm_data(dialog_manager: DialogManager, **kwargs):
    logger.debug(dialog_manager.dialog_data)

    if dialog_manager.dialog_data["icon"]:
        icon = MediaAttachment(
            type=ContentType.PHOTO,
            file_id=MediaId(dialog_manager.dialog_data["icon"]),
        )
    else:
        icon = ""

    return {
        "name": dialog_manager.dialog_data.get("name", ""),
        "description": dialog_manager.dialog_data.get(
            "description", "не указано"
        ),
        "icon": icon,
    }


create_campaign_dialog = Dialog(
    Window(
        Const("**Создание новой кампании**\n\nВведите название кампании:"),
        TextInput(
            id="name_input",
            on_success=on_name_entered,
        ),
        Cancel(Const("Отмена")),
        state=CreateCampaignStates.enter_name,
    ),
    Window(
        Const("**Введите описание кампании**\n\nМожно пропустить:"),
        TextInput(
            id="description_input",
            on_success=on_description_entered,
        ),
        Row(
            Button(
                Const("Пропустить"),
                id="skip_desc",
                on_click=on_skip_description,
            ),
            Back(Const("Назад")),
        ),
        Cancel(Const("Отмена")),
        state=CreateCampaignStates.enter_description,
    ),
    Window(
        Const("**Введите иконку для кампании**\n\nМожно пропустить:"),
        MessageInput(func=on_icon_entered, content_types=ContentType.PHOTO),
        Row(
            Button(Const("Пропустить"), id="skip_icon", on_click=on_skip_icon),
            Back(Const("Назад")),
        ),
        Cancel(Const("Отмена")),
        state=CreateCampaignStates.enter_icon,
    ),
    Window(
        DynamicMedia("icon", when="icon"),
        Format(
            "**Подтверждение создания**\n\n"
            "Название: {name}\n"
            "Описание: {description}\n"
            "Создать кампанию?"
        ),
        Button(Const("Создать"), id="confirm", on_click=on_confirm),
        Back(Const("Назад")),
        Cancel(Const("Отмена")),
        state=CreateCampaignStates.confirm,
        getter=get_confirm_data,
    ),
)

router.include_router(create_campaign_dialog)
