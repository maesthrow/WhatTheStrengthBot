import operator

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Button
from aiogram_dialog.widgets.text import Format, Const

from dialogs.general_handlers import main_menu_handler
from dialogs.persons import keyboards
from dialogs.persons.getters import get_person_select_data
from dialogs.persons.handlers import person_selected_handler, persons_on_page_changed_handler
from dialogs.widgets.wts_scrolling_group import WtsScrollingGroup
from states import PersonState

person_select_window = Window(
    Format("{message_text}"),
    WtsScrollingGroup(
        Select(
            Format("{item[title]}"),
            id='persons_select',
            item_id_getter=operator.itemgetter('_id'),
            items='persons',
            on_click=person_selected_handler
        ),
        id='persons_scroll',
        height=8,
        width=1,
        hide_on_single_page=True,
        on_page_changed=persons_on_page_changed_handler
    ),
    keyboards.sort_type_buttons(),
    Button(text=Const("☰ Меню"), id="main_menu", on_click=main_menu_handler),
    state=PersonState.PersonSelect,
    getter=get_person_select_data
)

dialog_persons = Dialog(
    person_select_window,
)
