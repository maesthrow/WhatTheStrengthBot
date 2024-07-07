from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedCheckbox, ManagedRadio

from data.videos_repository import get_persons_videos
from utils.converter import to_date_time


async def get_person_select_data(dialog_manager: DialogManager, **kwargs):
    user = dialog_manager.event.from_user
    message_text = '👥 Персоны, многие из которых гости YouTube-канала «вДудь», но и не только'

    persons = await get_persons_videos(user)

    selected_value = dialog_manager.current_context().widget_data.get('sort_type', 'rating')

    if not dialog_manager.current_context().widget_data.get('sort_type'):
        dialog_manager.current_context().widget_data['sort_type'] = 'rating'
    if dialog_manager.current_context().widget_data.get('sort_type', 'rating') == 'publish_date':
        sorted_persons = sorted(persons, key=lambda person: (to_date_time(person['publish_date']), person['title'].lower()),
                                reverse=True)
    else:
        sorted_persons = sorted(persons, key=lambda person: (-person['likes'], person['title'].lower()))
    # radioRating: ManagedRadio = dialog_manager.find('rating')
    # await radioRating.set_checked(True)
    dialog_manager.current_context().dialog_data = {'persons': sorted_persons}
    return {
        'message_text': message_text,
        'persons': sorted_persons,
        'selected_value': selected_value
    }
