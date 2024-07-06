from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from dialogs.main_menu.getters import get_main_menu_data
from dialogs.main_menu.handlers import select_persons_handler, send_playlist_handler
from dialogs.widgets.inline_query_button import InlineQueryButton
from states import MainMenuState

main_menu_window = Window(
    Format('{message_text}'),
    Button(Const('👥 Выбор персон'), id="select_persons", on_click=select_persons_handler),
    InlineQueryButton(Const('️🔍️ Поиск персон'), id="search_persons", switch_inline_query_current_chat=Const("")),
    Button(Const('🎶 Плейлист ответов'), id="send_playlist", on_click=send_playlist_handler),
    state=MainMenuState.Menu,
    getter=get_main_menu_data
)

dialog_main_menu = Dialog(
    main_menu_window,
)
