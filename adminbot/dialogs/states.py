from aiogram.fsm.state import State, StatesGroup


class CampaignManagerMain(StatesGroup):
    main = State()
    campaign_list = State()


class CampaignManage(StatesGroup):
    main = State()
    edit_info = State()
    manage_students = State()
    permissions = State()


class CreateCampaign(StatesGroup):
    select_title = State()
    select_description = State()
    select_icon = State()
    confirm = State()
