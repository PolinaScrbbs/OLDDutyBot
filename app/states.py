from aiogram.fsm.state import StatesGroup, State

class Auth(StatesGroup):
    login = State()
    password = State()

class GetAttendants(StatesGroup):
    wait = State()