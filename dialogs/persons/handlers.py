from datetime import datetime

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import DialogUpdateEvent
from aiogram_dialog.dialog import ChatEvent
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.kbd import Select, Button, ManagedCheckbox, ManagedRadio

from cards.person import send_video_card
from data.videos_repository import get_persons_videos
from states import MainMenuState, PersonState
from storage.data_manager import set_data, add_data
from utils.converter import to_date_time


async def person_selected_handler(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, person_video_id):
    chat_id = dialog_manager.event.from_user.id

    persons_scroll_page = dialog_manager.current_context().widget_data.get('persons_scroll')
    await add_data(chat_id, {'persons_scroll_page': persons_scroll_page})

    await send_video_card(chat_id, person_video_id)


async def persons_on_page_changed_handler(event: DialogUpdateEvent, managed_scroll: ManagedScroll, dialog_manager: DialogManager):
    chat_id = dialog_manager.event.from_user.id
    persons_scroll_page = dialog_manager.current_context().widget_data.get('persons_scroll')
    await add_data(chat_id, {'persons_scroll_page': persons_scroll_page})


async def sync_sort_type_change(c, b, d, item_id):
    dialog_manager: DialogManager = d
    value = item_id
    user = dialog_manager.event.from_user

    persons = await get_persons_videos(user)

    sorted_persons = []
    radioSortType: ManagedRadio = dialog_manager.find('sort_type')

    # radioRating: ManagedRadio = dialog_manager.find('rating')
    # radioPublishDate: ManagedRadio = dialog_manager.find('publish_date')
    if value == 'rating':
        await radioSortType.set_checked('rating')
        sorted_persons = sorted(persons, key=lambda person: (-person['likes'], person['title'].lower()))
    elif value == 'publish_date':
        await radioSortType.set_checked('publish_date')
        sorted_persons = sorted(persons, key=lambda person: (to_date_time(person['publish_date']), person['title'].lower()), reverse=True)

    dialog_manager.current_context().dialog_data = {'persons': sorted_persons}
    await dialog_manager.switch_to(state=PersonState.PersonSelect)
