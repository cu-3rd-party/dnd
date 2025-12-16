import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Row
from aiogram_dialog.widgets.text import Const, Format, Multi

from db.models import Invitation
from services.invitation import handle_accept_invitation, invitation_getter
from states.academy import Academy
from states.invitation import InvitationAccept
from states.start_simple import StartSimple

logger = logging.getLogger(__name__)
router = Router()


async def on_accept(msg: CallbackQuery, _: Button, dialog_manager: DialogManager):
    invite_id = dialog_manager.dialog_data.get("invite_id")
    if not invite_id:
        await msg.answer("❌ Приглашение не найдено", show_alert=True)
        await dialog_manager.reset_stack()
        return

    invite = await Invitation.get_or_none(id=invite_id).prefetch_related("campaign", "created_by")
    if invite is None:
        await msg.answer("❌ Приглашение не найдено", show_alert=True)
        await dialog_manager.reset_stack()
        return

    user = dialog_manager.middleware_data["user"]

    participation = await handle_accept_invitation(dialog_manager, msg, user, invite)

    if invite.campaign.verified:
        await dialog_manager.start(
            StartSimple.simple,
            data={
                "campaign_id": invite.campaign.id,
                "participation_id": participation.id,
                "redirect_to": Academy.main,
                "path": [
                    "AcademyCampaigns.campaigns",
                    "AcademyCampaignPreview.preview",
                ],
            },
            mode=StartMode.RESET_STACK,
        )
    else:
        # TODO @pxc1984: когда доделаем другие игры следует сюда добавить логику активации игры для них
        #   https://github.com/cu-tabletop/dnd/issues/10
        pass


invite_dialog = Dialog(
    Window(
        Multi(
            Const("🎉 Вам пришло приглашение!"),
            Const(""),
            Format("🏰 Кампания: <b>{campaign_title}</b>"),
            Format("👑 Роль: <b>{role}</b>"),
            Const(""),
            Const("Присоединиться к кампании?"),
            sep="\n",
        ),
        Row(
            Button(Const("✅ Присоединиться"), id="accept_admin", on_click=on_accept),
            Cancel(Const("❌ Отказаться")),
        ),
        getter=invitation_getter,
        state=InvitationAccept.invitation,
    )
)

router.include_router(invite_dialog)
