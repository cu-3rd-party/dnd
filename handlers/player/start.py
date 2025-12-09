import logging

from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column
from aiogram_dialog.widgets.text import Const

from db.models import Invitation, User
from utils.uuid import is_valid_uuid
from states.academy import Academy
from states.invitation import InvitationAccept
from states.start_simple import StartSimple
from states.upload_character import UploadCharacter

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart(deep_link=True))
async def start_args(message: Message, command: CommandObject, dialog_manager: DialogManager, user: User):
    if not command.args:
        return
    if not is_valid_uuid(command.args):
        logger.warning("User %s used /start with invalid UUID: %s", user.id, command.args)
        return
    invite = await Invitation.get_or_none(start_data=command.args).prefetch_related("user", "campaign")
    if not invite:
        logger.warning(
            "User %s used /start with arguments %s that weren't in the invitations",
            user.id,
            command.args,
        )
        return
    if invite.user is None:
        invite.user = user
        await invite.save()
    elif invite.user.id != user.id:
        logger.warning(
            "User %s used /start with arguments %s that wasn't for him. It was for %s",
            user.id,
            command.args,
            invite.user.id,
        )
        return
    logger.info("%s пригласили в игру %s на роль %s", invite.user.id, invite.campaign.id, invite.role.name)
    if invite.used:
        await message.reply(
            "Сорян, этот инвайт уже был использован.\n\n"
            "Если ты его использовал по ошибке, то попроси мастера пригласить тебя еще раз"
        )
        return
    logger.debug(
        "Такой инвайт был найден. %s пригласили в игру %s на роль %s",
        invite.user.id,
        invite.campaign.id,
        invite.role.name,
    )

    invite.used = True
    await invite.save()

    await dialog_manager.start(InvitationAccept.invitation, data={"invitation_id": invite.id})


@router.message(CommandStart(deep_link=False))
async def start_simple(message: Message, dialog_manager: DialogManager, user: User):
    await dialog_manager.start(StartSimple.simple)


async def on_academy(c: CallbackQuery, b: Button, m: DialogManager):
    user: User = m.middleware_data["user"]
    if user.data is None:
        await m.start(UploadCharacter.upload, data={"source": "user"})
        return
    await m.start(Academy.main)


async def on_other(c: CallbackQuery, b: Button, m: DialogManager): ...


router.include_router(
    Dialog(
        Window(
            Const("Обычный /start"),
            Column(
                Button(Const("Академия"), id="academy", on_click=on_academy),
                Button(Const("Другие игры"), id="other_games", on_click=on_other),
                # TODO (@pxc1984): Добавить ближайшие встречи
                #    https://github.com/cu-tabletop/dnd/issues/11
            ),
            state=StartSimple.simple,
        )
    )
)
