from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from enums import PlaylistType
from states import PersonState, MainMenuState
from utils.playlist import send_playlist


async def select_persons_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(PersonState.PersonSelect)


async def select_playlist_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainMenuState.Playlists)


async def statistic_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainMenuState.Statistic)


async def send_playlist_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    btn_text = await button.text.render_text(dialog_manager.current_context().widget_data, dialog_manager)
    await send_playlist(callback.message, PlaylistType.from_value(btn_text))


async def contact_developer_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    pass
