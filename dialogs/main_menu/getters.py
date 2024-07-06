from aiogram_dialog import DialogManager

from utils.text import INVISIBLE_CHAR


async def get_main_menu_data(dialog_manager: DialogManager, **kwargs):
    return {'message_text': f'<b>☰ Меню</b>{INVISIBLE_CHAR * 40}'}
