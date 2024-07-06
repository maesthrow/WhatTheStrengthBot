from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from states import PersonState
from utils.playlist import send_playlist


async def select_persons_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(PersonState.PersonSelect)


async def send_playlist_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await send_playlist(callback.message)
