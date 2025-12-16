import json

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Column, Row
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from db.models import Campaign, Character, Participation, User
from services.character_data import character_preview_getter
from states.inventory_view import InventoryView, TargetType
from states.other_games_campaign import OtherGamesCampaign
from states.other_games_character import OtherGamesCharacter
from states.upload_character import UploadCharacter

router = Router()


async def character_data_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    character = await Character.get(id=dialog_manager.start_data["character_id"])
    data = json.loads(character.data["data"])

    character_preview = character_preview_getter(character, data)

    return {
        **character_preview,
        "has_character_data": character_preview.get("character_data_preview") not in [None, ""],
    }


async def on_campaign_info(c: CallbackQuery, b: Button, m: DialogManager):
    user: User = m.middleware_data["user"]
    character = await Character.get(id=m.start_data["character_id"]).prefetch_related("campaign")
    campaign: Campaign = character.campaign
    participation = await Participation.get(user=user, campaign=campaign)
    await m.start(
        OtherGamesCampaign.preview,
        data={
            **m.start_data,
            "campaign_id": campaign.id,
            "participation_id": participation.id,
        },
    )


async def on_inventory(c: CallbackQuery, b: Button, m: DialogManager):
    character = await Character.get(id=m.start_data["character_id"]).prefetch_related("campaign")
    campaign: Campaign = character.campaign
    await m.start(
        InventoryView.view,
        data={
            "target_type": TargetType.CHARACTER,
            "target_id": m.start_data["character_id"],
            "campaign_id": campaign.id,
        },
    )


async def on_upload_json(c: CallbackQuery, b: Button, m: DialogManager):
    await m.start(
        UploadCharacter.upload,
        data={
            "target_type": TargetType.CHARACTER,
            "target_id": None,
            "campaign_id": m.start_data.get("campaign_id"),
        },
    )


character_dialog = Dialog(
    Window(
        Multi(
            Const("👤 Персонаж"),
            Const(""),
        ),
        DynamicMedia("avatar", when="avatar"),
        Format("{character_data_preview}", when="character_data_preview"),
        Const("📭 У персонажа нет данных", when=lambda data, *_: not data.get("character_data_preview", "")),
        Column(
            Row(
                Button(Const("🎒 Инвентарь"), id="inventory", on_click=on_inventory),
                Button(Const("🏰 Кампания"), id="campaign_info", on_click=on_campaign_info),
            ),
            Button(Const("📤 Обновить .json"), id="update_json", on_click=on_upload_json),
            Cancel(Const("⬅️ Назад")),
        ),
        getter=character_data_getter,
        state=OtherGamesCharacter.preview,
    )
)

router.include_router(character_dialog)
