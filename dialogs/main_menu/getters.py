from aiogram_dialog import DialogManager

from utils.entities import get_entities_statistic
from utils.text import INVISIBLE_CHAR


async def get_main_menu_data(dialog_manager: DialogManager, **kwargs):
    return {'message_text': f'<b>☰ Меню</b>{INVISIBLE_CHAR * 40}'}


async def get_statistic_data(dialog_manager: DialogManager, **kwargs):
    statistic = await get_entities_statistic()
    message_text = f'📊 <b>Статистика упоминаний</b>\n\n{'\n'.join(statistic)}'
    return {'message_text': message_text}