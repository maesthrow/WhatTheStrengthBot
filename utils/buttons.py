from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import PersonSelectCallback, PersonLikeCallback, MainMenuCallback
from utils.bot import get_bot_name, get_bot_link
from utils.text import INVISIBLE_CHAR
from utils.user import EMPTY_LIKE_ICON, SET_LIKE_ICON


def get_start_markup():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='☰ Меню',
            callback_data=MainMenuCallback().pack(),
        )
    )
    return builder.as_markup()


def get_person_video_card_keyboard(video_id, like_icon: str, likes_count: int) -> InlineKeyboardMarkup:
    like_action_result = 1 if like_icon == EMPTY_LIKE_ICON else -1
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f'{like_icon} {likes_count}',
        callback_data=PersonLikeCallback(result=like_action_result, video_id=video_id).pack()
    )
    builder.button(
        text="Поделиться", # ↗️
        switch_inline_query=f'id={video_id}',
    )
    builder.button(
        text="👥 Выбор персон",
        callback_data=PersonSelectCallback().pack()
    )
    builder.adjust(2, 1)
    return builder.as_markup()


async def get_inline_repost_markup(video_id):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=f'Бот «{await get_bot_name()}»',
            url=f"{await get_bot_link()}?start={video_id}",
        )
    )
    return builder.as_markup()


async def get_inline_goto_person_markup(video_id):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=f'✨ Раскрыть персону',
            url=f"{await get_bot_link()}?start={video_id}",
        )
    )
    return builder.as_markup()


def get_inline_search_markup():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=f'Нажмите, чтобы активировать поиск',
            switch_inline_query_current_chat=''
        ),
        InlineKeyboardButton(
            text=f'☰ Меню',
            callback_data=MainMenuCallback().pack(),
        )
    )
    builder.adjust(1, 1)
    return builder.as_markup()
