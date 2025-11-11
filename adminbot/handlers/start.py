from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dialogs import states as campaign_states

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, dialog_manager: DialogManager):
    user = message.from_user
    welcome_text = (
        f"Приветствую вас, Мастер {user.first_name}!\n\n"  # type: ignore
        "Я ваш верный помощник в организации настольных ролевых игр.\n"
        # "С моей помощью вы сможете:\n"
        # "• Создавать и управлять игровыми кампаниями\n"
        # "• Контролировать персонажей игроков\n"
        # "• Настраивать права доступа для участников\n"
        # "• Хранить всю информацию о вашем мире\n\n"
        "Давайте начнем наше приключение!"
    )

    await message.answer(welcome_text)

    await dialog_manager.start(
        state=campaign_states.CampaignManagerMain.main,
        mode=StartMode.RESET_STACK,
        data={"user_id": user.id},  # type: ignore
    )
