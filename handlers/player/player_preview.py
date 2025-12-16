import json
import logging

from aiogram import Router
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Cancel, Row, Url
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from db.models import User
from services.character_data import character_preview_getter
from states.player_preview import PlayerPreview

logger = logging.getLogger(__name__)
router = Router()


async def preview_getter(dialog_manager: DialogManager, **kwargs):
    if "light" not in dialog_manager.dialog_data and isinstance(dialog_manager.start_data, dict):
        dialog_manager.dialog_data["light"] = dialog_manager.start_data.get("light", True)
        dialog_manager.dialog_data["user_id"] = dialog_manager.start_data.get("user_id", 0)

    user = await User.get(id=dialog_manager.dialog_data["user_id"])
    data = json.loads(user.data["data"])
    light = dialog_manager.dialog_data["light"]

    character_preview = character_preview_getter(user, data, light=light)

    return {
        "profile_link": f"tg://user?id={user.id}",
        "username": user.username or "Пользователь",
        **character_preview,
        "has_character_data": character_preview.get("character_data_preview") not in [None, ""],
    }


preview_dialog = Dialog(
    Window(
        Multi(
            Format("👤 Профиль: @{username}"),
            Const(""),
        ),
        DynamicMedia("avatar", when="avatar"),
        Format("{character_data_preview}", when="character_data_preview"),
        Const(
            "📭 У игрока нет загруженного персонажа", when=lambda data, *_: not data.get("character_data_preview", "")
        ),
        Row(
            Url(Const("📨 Написать"), Format("{profile_link}")),
            Cancel(Const("⬅️ Назад")),
        ),
        getter=preview_getter,
        state=PlayerPreview.preview,
    )
)

router.include_router(preview_dialog)
