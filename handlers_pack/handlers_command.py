from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from cards.person import send_video_card
from load_all import dp, bot
from mongo_db.mongo_collection_users import has_user, add_user
from states import PersonState, MainMenuState
from storage.data_manager import add_data
from utils.buttons import get_inline_search_markup, get_start_markup
from utils.data import remove_publish_dates, reset_publish_dates_to_str
from utils.entities import load_entities, get_entities_statistic
from utils.playlist import send_playlist

router = Router()
dp.include_router(router)


@router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    # print(message.text)
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
    await bot.send_message(chat_id, '<b>Поехали</b> 🚀', reply_markup=get_start_markup())
    # await set_video_additional_default_data()
    # await remove_publish_dates()
    # await reset_publish_dates_to_str()


@router.message(Command(commands=["select"]))
async def select_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    await add_data(message.from_user.id, {'persons_scroll_page': 0})  # устанавливаем на 1-ю страницу
    await dialog_manager.start(PersonState.PersonSelect)


@router.message(Command(commands=["statistic"]))
async def select_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    statistic = await get_entities_statistic()
    await bot.send_message(message.chat.id, f'📊 <b>Статистика упоминаний</b>\n\n{'\n'.join(statistic)}')


@router.message(Command(commands=["search"]))
async def search_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    tg_user = message.from_user
    await message.answer(
        "️🔍️",
        reply_markup=get_inline_search_markup()
    )


@router.message(Command(commands=["playlist"]))
async def playlists_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    await dialog_manager.start(MainMenuState.Playlists)


@router.message(Command(commands=["contact"]))
async def playlists_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    await bot.send_message(message.chat.id, '<b>Обратная связь</b> 💬')


@router.message(Command(commands=["help"]))
async def help_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    tg_user = message.from_user
    await bot.send_message(message.chat.id, 'Помощь')


@router.message(F.via_bot != None)
async def via_bot_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    pass
