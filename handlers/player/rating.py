import json
import logging

import tortoise.exceptions
from aiogram import Router
from aiogram.enums import ContentType
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, Dialog, Window
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Column, Button, Cancel, ScrollingGroup, Select, Url, Back
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from db.models import Invite, User
from services.character import CharacterData, parse_character_data
from services.character_data import character_preview_getter
from states.academy import Academy
from states.rating import AcademyRating
from states.start_simple import StartSimple
from states.upload_character import UploadCharacter

logger = logging.getLogger(__name__)
router = Router()


async def rating_getter(dialog_manager: DialogManager, **kwargs):
    return {"top": await User.all().order_by("-rating")}


async def preview_getter(dialog_manager: DialogManager, **kwargs):
    user = await User.get(id=dialog_manager.dialog_data["preview_id"])
    data = json.loads(user.data["data"])

    return {
        "profile_link": f"tg://user?id={user.id}",
        **character_preview_getter(user, data),
    }


async def on_preview(c: CallbackQuery, b: Button, m: DialogManager, user_id: int):
    m.dialog_data["preview_id"] = user_id
    await m.switch_to(AcademyRating.preview)


router.include_router(
    Dialog(
        Window(
            Const("Вот топ по рейтингу"),
            ScrollingGroup(
                Select(
                    Format("@{item.username} - {item.rating}"),
                    id="preview",
                    items="top",
                    item_id_getter=lambda x: x.id,
                    on_click=on_preview,
                ),
                hide_on_single_page=True,
                height=5,
                id="top",
            ),
            Cancel(Const("Назад")),
            getter=rating_getter,
            state=AcademyRating.rating,
        ),
        Window(
            DynamicMedia("avatar", when="avatar"),
            Format("{character_data_preview}", when="character_data_preview"),
            Url(Const("Перейти в профиль"), Format("{profile_link}")),
            Back(Const("Назад")),
            getter=preview_getter,
            state=AcademyRating.preview,
        ),
    )
)
