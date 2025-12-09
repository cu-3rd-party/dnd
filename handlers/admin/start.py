import logging

from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from db.models import Invitation, User
from utils.uuid import is_valid_uuid

from . import states

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

    await dialog_manager.start(states.InviteMenu.invite, data={"invitation_id": invite.id})


@router.message(CommandStart(deep_link=False))
async def cmd_start(message: Message, dialog_manager: DialogManager):
    user: User = dialog_manager.middleware_data["user"]

    welcome_text = (
        f"Приветствую вас, Мастер {user.username}!\n\n"
        "Я ваш верный помощник в организации настольных ролевых игр.\n"
        "Давайте начнем наше приключение!"
    )

    await message.answer(welcome_text)

    await dialog_manager.start(
        state=states.CampaignList.main,
        mode=StartMode.RESET_STACK,
        data={"user_id": user.id},
    )
