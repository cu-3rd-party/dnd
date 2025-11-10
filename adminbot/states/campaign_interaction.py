from aiogram.fsm.state import StatesGroup, State


class CampaignInteractionStates(StatesGroup):
    main = State()
    characters = State()
    add_admins = State()
