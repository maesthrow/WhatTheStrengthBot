from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from dialogs.general_handlers import main_menu_handler
from dialogs.main_menu.getters import get_main_menu_data
from dialogs.main_menu.handlers import select_persons_handler, select_playlist_handler, \
    send_playlist_handler, contact_developer_handler
from dialogs.widgets.inline_query_button import InlineQueryButton
from enums import PlaylistType
from states import MainMenuState

main_menu_window = Window(
    Format('{message_text}'),
    Button(Const('👥 Выбор персон'), id="select_persons", on_click=select_persons_handler),
    InlineQueryButton(Const('️🔍️ Поиск персон'), id="search_persons", switch_inline_query_current_chat=Const("")),
    Button(Const('🎧 Плейлисты ответов'), id="send_playlist", on_click=select_playlist_handler),
    Button(Const('‍👨‍💻 Написать разработчику'), id="contact_developer", on_click=contact_developer_handler),
    state=MainMenuState.Menu,
    getter=get_main_menu_data
)

playlists_window = Window(
    Const('🎧 Плейлисты ответов'),
    Button(Const(PlaylistType.Top10.value), id="top10_playlist", on_click=send_playlist_handler),
    Button(Const(PlaylistType.Top20.value), id="top20_playlist", on_click=send_playlist_handler),
    Button(Const(PlaylistType.New.value), id="new_playlist", on_click=send_playlist_handler),
    Button(Const(PlaylistType.Chronology.value), id="all_chronology_playlist", on_click=send_playlist_handler),
    Button(Const(PlaylistType.Rating.value), id="all_rating_playlist", on_click=send_playlist_handler),
    Button(text=Const("☰ Меню"), id="main_menu", on_click=main_menu_handler),
    state=MainMenuState.Playlists,
)

dialog_main_menu = Dialog(
    main_menu_window,
    playlists_window
)
