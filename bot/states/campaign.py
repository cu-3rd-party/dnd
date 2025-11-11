from aiogram.fsm.state import StatesGroup, State


class CampaignDialog(StatesGroup):
    preview = State()
    upload = State()
