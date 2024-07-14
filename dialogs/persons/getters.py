from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedCheckbox, ManagedRadio

from data.videos_repository import get_persons_videos
from storage.data_manager import get_data
from utils.converter import to_date_time


async def get_person_select_data(dialog_manager: DialogManager, **kwargs):
    user = dialog_manager.event.from_user
    message_text = '👥 <b>Персоны, многие из которых гости YouTube-канала «вДудь», но и не только</b>'

    persons = await get_persons_videos(user)

    selected_value = dialog_manager.current_context().widget_data.get('sort_type', 'rating')

    if not dialog_manager.current_context().widget_data.get('sort_type'):
        dialog_manager.current_context().widget_data['sort_type'] = 'rating'
    if dialog_manager.current_context().widget_data.get('sort_type', 'rating') == 'publish_date':
        sorted_persons = sorted(persons, key=lambda person: (to_date_time(person['publish_date']), person['title'].lower()),
                                reverse=True)
    else:
        sorted_persons = sorted(persons, key=lambda person: (-person['likes'], person['title'].lower()))

    storage_data = await get_data(user.id)

    dialog_manager.current_context().widget_data['persons_scroll'] = storage_data.get('persons_scroll_page', 0)

    dialog_manager.current_context().dialog_data = {'persons': sorted_persons}
    return {
        'message_text': message_text,
        'persons': sorted_persons,
        'selected_value': selected_value,
        # 'persons_scroll_page': storage_data.get('persons_scroll_page', 0)
    }
