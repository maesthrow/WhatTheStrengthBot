import operator

from aiogram_dialog.widgets.kbd import Row, Checkbox, Radio
from aiogram_dialog.widgets.text import Const, Text, Format

from dialogs.persons.handlers import sync_sort_type_change


def sort_type_buttons():
    return Radio(
            Format("🔘 {item[1]}"),  # 🟢 🔘
            Format("⚪️ {item[1]}"),
            id='sort_type',
            item_id_getter=operator.itemgetter(0),
            items=[('rating', 'Рейтинг'), ('publish_date', 'Дата публикации')],
            on_click=sync_sort_type_change,
        )



