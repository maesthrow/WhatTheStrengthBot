from aiogram.fsm.state import StatesGroup, State


class MainMenuState(StatesGroup):
    Menu = State()
    Playlists = State()


class PersonState(StatesGroup):
    PersonSelect = State()