from aiogram.fsm.state import StatesGroup, State


class MainMenuState(StatesGroup):
    Menu = State()


class PersonState(StatesGroup):
    PersonSelect = State()