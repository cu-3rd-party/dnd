import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Const, Format

from db.models import Invitation
from services.invitation import handle_accept_invitation, invitation_getter
from states.academy_campaigns import AcademyCampaignPreview
from states.invitation import InvitationAccept
from utils.invitation import get_invite_id

logger = logging.getLogger(__name__)
router = Router()


async def on_accept(c: CallbackQuery, b: Button, m: DialogManager):
    invite_id = get_invite_id(m)
    invitation = await Invitation.get_or_none(id=invite_id).prefetch_related("campaign", "created_by")

    if invitation is None:
        msg = "Invitation not found"
        raise ValueError(msg)

    user = m.middleware_data["user"]

    participation = await handle_accept_invitation(m, c, user, invitation)

    if invitation.campaign.verified:
        await m.start(
            AcademyCampaignPreview.preview,
            data={"campaign_id": invitation.campaign.id, "participation_id": participation.id},
        )
    else:
        # TODO @pxc1984: когда доделаем другие игры следует сюда добавить логику активации игры для них
        #   https://github.com/cu-tabletop/dnd/issues/10
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
