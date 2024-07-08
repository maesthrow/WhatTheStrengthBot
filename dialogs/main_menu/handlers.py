from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from states import PersonState, MainMenuState
from utils.playlist import send_playlist


async def select_persons_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(PersonState.PersonSelect)


async def select_playlist_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainMenuState.Playlists)


async def send_all_rating_playlist_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await send_playlist(callback.message)


async def contact_developer_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    pass
