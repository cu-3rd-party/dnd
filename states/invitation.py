from aiogram.fsm.state import StatesGroup, State


class InvitationAccept(StatesGroup):
    invitation = State()
