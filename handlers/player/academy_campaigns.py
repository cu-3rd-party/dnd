import logging
from uuid import UUID

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Select
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from db.models import Participation
from services.campaigns import campaign_getter
from states.academy_campaigns import AcademyCampaignPreview, AcademyCampaigns
from utils.redirect import redirect

logger = logging.getLogger(__name__)
router = Router()


async def campaigns_getter(dialog_manager: DialogManager, **kwargs):
    user = dialog_manager.middleware_data["user"]
    participations = await Participation.filter(user=user, campaign__verified=True).prefetch_related("campaign").all()

    return {
        "campaigns": participations,
        "has_campaigns": len(participations) > 0,
    }


async def on_campaign(c: CallbackQuery, b: Select, m: DialogManager, participation_id: UUID):
    participation = await Participation.get(id=participation_id).prefetch_related("campaign")
    await m.start(
        AcademyCampaignPreview.preview,
        data={"campaign_id": participation.campaign.id, "participation_id": participation.id},
    )


# Диалог списка кампаний академии
campaigns_dialog = Dialog(
    Window(
        Multi(
            Const("🏰 Кампании академии"),
            Const(""),
            Const("Здесь собраны официальные кампании, в которых вы участвуете."),
            Const(""),
            Const("📭 У вас пока нет кампаний в академии", when=lambda data, *_: not data.get("has_campaigns", False)),
            sep="\n",
        ),
        ScrollingGroup(
            Select(
                Format("🎮 {item.campaign.title}"),
                id="campaign",
                items="campaigns",
                item_id_getter=lambda x: x.id,
                on_click=on_campaign,
                type_factory=UUID,
            ),
            hide_on_single_page=True,
            height=5,
            id="campaigns",
            when="has_campaigns",
        ),
        Cancel(Const("⬅️ Назад")),
        getter=campaigns_getter,
        state=AcademyCampaigns.campaigns,
    ),
    on_start=redirect,
)


# Диалог предпросмотра кампании
preview_dialog = Dialog(
    Window(
        DynamicMedia("icon"),
        Multi(
            Format("🎓 Информация о кампании: {title}"),
            Const(""),
            Format("📝 Описание: {description}"),
            Const(""),
            Const("Здесь вы можете управлять своей кампанией."),
            sep="\n",
        ),
        Cancel(Const("⬅️ Назад")),
        getter=campaign_getter,
        state=AcademyCampaignPreview.preview,
    ),
    on_start=redirect,
)

router.include_routers(campaigns_dialog, preview_dialog)
