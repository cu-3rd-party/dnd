import json
import logging
from uuid import UUID

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
from pydantic.v1 import UUID4

from db.models import Invitation, User, Campaign, Participation
from services.character import CharacterData, parse_character_data
from services.character_data import character_preview_getter
from states.academy import Academy
from states.academy_campaigns import AcademyCampaigns, AcademyCampaignPreview
from states.invitation import InvitationAccept
from states.rating import AcademyRating
from states.start_simple import StartSimple
from states.upload_character import UploadCharacter

logger = logging.getLogger(__name__)
router = Router()


async def invitation_getter(dialog_manager: DialogManager, **kwargs):
    invitation = await Invitation.get_or_none(id=dialog_manager.start_data["invitation_id"]).prefetch_related(
        "campaign"
    )
    return {
        "campaign_title": invitation.campaign.title,
        "role": invitation.role.name,
    }


async def on_accept(c: CallbackQuery, b: Button, m: DialogManager):
    invitation = await Invitation.get_or_none(id=m.start_data["invitation_id"]).prefetch_related("campaign")
    participation = await Participation.create(
        user=m.middleware_data["user"], campaign=invitation.campaign, role=invitation.role
    )
    await c.answer(f"Приглашение в кампанию {invitation.campaign.title} принято!")
    await m.done()
    if invitation.campaign.verified:
        await m.start(
            AcademyCampaignPreview.preview,
            data={"campaign_id": invitation.campaign.id, "participation_id": participation.id},
        )
    else:
        # TODO:
        ...


router.include_router(
    Dialog(
        Window(
            Format("Вас пригласили в кампанию <b>{campaign_title}</b> на роль <b>{role}</b>"),
            Button(Const("Присоединиться"), id="accept", on_click=on_accept),
            Cancel(Const("Отказаться")),
            getter=invitation_getter,
            state=InvitationAccept.invitation,
        )
    )
)
