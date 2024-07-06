from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode

from callback_data import PersonSelectCallback, PersonLikeCallback, MainMenuCallback
from data.users_repository import set_user_likes
from data.videos_repository import set_video_likes
from load_all import dp, bot
from states import PersonState, MainMenuState
from utils.buttons import get_person_video_card_keyboard
from utils.user import SET_LIKE_ICON, EMPTY_LIKE_ICON

router = Router()
dp.include_router(router)


@router.callback_query(MainMenuCallback.filter())
async def main_menu_handler(call: CallbackQuery, callback_data: MainMenuCallback, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenuState.Menu)


@router.callback_query(PersonSelectCallback.filter())
async def persons_handler(call: CallbackQuery, callback_data: PersonSelectCallback, dialog_manager: DialogManager):
    await dialog_manager.start(PersonState.PersonSelect, show_mode=ShowMode.SEND)
    await call.answer()


@router.callback_query(PersonLikeCallback.filter())
async def person_set_like_handler(call: CallbackQuery, callback_data: PersonLikeCallback, dialog_manager: DialogManager):
    video_id = callback_data.video_id
    like_action_result = callback_data.result
    if await set_video_likes(video_id, like_action_result):
        if not await set_user_likes(call.from_user.id, video_id):
            await set_video_likes(video_id, -like_action_result)
        else:
            markup = call.message.reply_markup
            likes_count = int(markup.inline_keyboard[0][0].text.split()[-1]) + like_action_result
            like_icon = SET_LIKE_ICON if like_action_result == 1 else EMPTY_LIKE_ICON
            markup = get_person_video_card_keyboard(video_id, like_icon, likes_count)
            await bot.edit_message_reply_markup(
                chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=markup
            )
    await call.answer()

