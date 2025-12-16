import json
import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Column, Row
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from services.character_data import character_preview_getter
from states.academy import Academy
from states.academy_campaigns import AcademyCampaigns
from states.inventory_view import InventoryView, TargetType
from states.rating import AcademyRating
from states.upload_character import UploadCharacter
from utils.redirect import redirect

logger = logging.getLogger(__name__)
router = Router()


async def on_inventory(c: CallbackQuery, b: Button, m: DialogManager):
    await m.start(InventoryView.view, data={"target_type": TargetType.USER, "target_id": m.middleware_data["user"].id})


async def on_update(c: CallbackQuery, b: Button, m: DialogManager):
    await m.start(
        UploadCharacter.upload,
        data={"target_type": TargetType.USER, "target_id": m.middleware_data["user"].id},
    )


async def on_rating(c: CallbackQuery, b: Button, m: DialogManager):
    await m.start(AcademyRating.rating)


async def on_campaigns(c: CallbackQuery, b: Button, m: DialogManager):
    await m.start(AcademyCampaigns.campaigns)


async def character_data_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    user = dialog_manager.middleware_data["user"]

    if user.data is None:
        return {"has_character_data": False, "avatar": False}

    data = json.loads(user.data.get("data", "{}"))

    character_preview = character_preview_getter(user, data)

    return {
        **character_preview,
        "has_character_data": True,
    }


academy_dialog = Dialog(
    Window(
        Multi(
            Const("🎓 Ваш профиль в академии"),
            Const(""),
        ),
        DynamicMedia("avatar", when="avatar"),
        Format("{character_data_preview}", when="has_character_data"),
        Const(
            "📭 У вас пока нет загруженного персонажа", when=lambda data, *_: not data.get("has_character_data", False)
        ),
        Column(
            Row(
                Button(Const("🏰 Кампании"), id="campaigns", on_click=on_campaigns),
                Button(Const("🎒 Инвентарь"), id="inventory", on_click=on_inventory),
            ),
            Row(
                Button(Const("📈 Рейтинг"), id="rating", on_click=on_rating),
                Button(Const("📤 Обновить .json"), id="update_json", on_click=on_update),
            ),
            Cancel(Const("⬅️ Назад")),
        ),
        getter=character_data_getter,
        state=Academy.main,
    ),
    on_start=redirect,
)

router.include_router(academy_dialog)
