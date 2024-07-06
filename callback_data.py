from aiogram.filters.callback_data import CallbackData


class MainMenuCallback(CallbackData, prefix="main_menu"):
    pass


class PersonSelectCallback(CallbackData, prefix="person_select"):
    pass


class PersonLikeCallback(CallbackData, prefix="person_like"):
    video_id: str
    result: int
