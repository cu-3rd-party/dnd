from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from db.models import Character
from services.campaigns import campaign_getter
from states.inventory_view import TargetType
from states.other_games_campaign import OtherGamesCampaign
from states.upload_character import UploadCharacter

router = Router()


async def campaign_preview_getter(dialog_manager: DialogManager, **kwargs):
    if "campaign_id" not in dialog_manager.dialog_data and isinstance(dialog_manager.start_data, dict):
        dialog_manager.dialog_data["campaign_id"] = dialog_manager.start_data.get("campaign_id", 0)
    campaign_id = dialog_manager.dialog_data["campaign_id"]
    user = dialog_manager.middleware_data["user"]

    character: Character | None = await Character.get_or_none(campaign_id=campaign_id, user=user)
    return {
        **await campaign_getter(dialog_manager, **kwargs),
        "should_join": character is None,
        "has_character": character is not None,
    }


async def on_join_campaign(c: CallbackQuery, b: Button, m: DialogManager):
    await m.start(
        UploadCharacter.upload,
        data={
            "target_type": TargetType.CHARACTER,
            "target_id": None,
            "campaign_id": m.dialog_data["campaign_id"],
        },
    )


campaign_preview_dialog = Dialog(
    Window(
        DynamicMedia("icon"),
        Multi(
            Format("🎮 Кампания: {title}"),
            Const(""),
            Format("📝 Описание: {description}"),
            Const(""),
            Const("🌟 Вы ещё не создали персонажа для этой кампании", when="should_join"),
            Const("✅ У вас уже есть персонаж в этой кампании", when="has_character"),
            sep="\n",
        ),
        Button(Const("➕ Присоединиться"), id="join", on_click=on_join_campaign, when="should_join"),
        Cancel(Const("⬅️ Назад")),
        getter=campaign_preview_getter,
        state=OtherGamesCampaign.preview,
    )
)

router.include_router(campaign_preview_dialog)
