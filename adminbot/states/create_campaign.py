from aiogram.fsm.state import StatesGroup, State


class CreateCampaignStates(StatesGroup):
    enter_name = State()
    enter_description = State()
    enter_icon = State()
    confirm = State()
