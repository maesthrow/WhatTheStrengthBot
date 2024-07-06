from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from cards.person import send_video_card
from load_all import dp, bot
from mongo_db.mongo_collection_users import has_user, add_user
from states import PersonState
from utils.buttons import get_inline_search_markup, get_start_markup
from utils.data import remove_publish_dates
from utils.playlist import send_playlist

router = Router()
dp.include_router(router)


@router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    #print(message.text)
    tg_user = message.from_user
    chat_id = message.chat.id
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    if len(args) == 1:
        person_video_id = args[0]
        await send_video_card(chat_id, person_video_id)
    else:
        await start(tg_user, chat_id)


async def start(tg_user, chat_id):
    if not await has_user(tg_user):
        await add_user(tg_user)
    await bot.send_message(chat_id, 'Поехали 🚀', reply_markup=get_start_markup())
    # await set_video_additional_default_data()
    # await remove_publish_dates()


@router.message(Command(commands=["select"]))
async def select_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    await dialog_manager.start(PersonState.PersonSelect)


@router.message(Command(commands=["search"]))
async def search_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    tg_user = message.from_user
    await message.answer(
        "️🔍️",
        reply_markup=get_inline_search_markup()
    )


@router.message(Command(commands=["playlist"]))
async def playlist_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    await send_playlist(message)


@router.message(Command(commands=["help"]))
async def help_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    tg_user = message.from_user
    await bot.send_message(message.chat.id, 'Помощь')


@router.message(F.via_bot != None)
async def via_bot_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    pass



