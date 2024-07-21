from aiogram.fsm.state import StatesGroup, State


class MainMenuState(StatesGroup):
    Menu = State()
    Playlists = State()
    Statistic = State()


class PersonState(StatesGroup):
    PersonSelect = State()