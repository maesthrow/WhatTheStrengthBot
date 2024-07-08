import hashlib
from typing import Union

from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.types import InlineQueryResultAudio, InlineQueryResultArticle, InlineQueryResultPhoto
from aiogram_dialog import DialogManager

from data.videos_repository import get_search_persons_videos
from load_all import dp, bot
from mongo_db.mongo_collection_videos import get_video_data
from utils.buttons import get_inline_repost_markup, get_inline_goto_person_markup
from utils.filename import get_splitter
from utils.text import escape_markdown

router = Router()
dp.include_router(router)


@router.inline_query(lambda query: 'id=' in query.query)
async def inline_query_handler(query: Union[types.InlineQuery]):  # , types.CallbackQuery]):
    video_id = query.query.split('id=')[-1]
    video_data = await get_video_data(video_id)
    markup = await get_inline_repost_markup(video_id)
    result_id = hashlib.md5(video_id.encode()).hexdigest()
    result = InlineQueryResultAudio(
        id=result_id,
        audio_url=video_data['tg_audio_id'],
        title=video_data['title'],
        caption=f'В чем сила?\n\n<tg-spoiler>{video_data['thesis']}</tg-spoiler>',
        reply_markup=markup
    )
    await bot.answer_inline_query(
        query.id,
        results=[result],
        cache_time=60,
    )


@router.inline_query(lambda query: not query.query.startswith('id='))
async def inline_query_search_handler(query: Union[types.InlineQuery]):
    search_results = []
    persons_videos = await get_search_persons_videos(query.from_user, query.query)
    sorted_persons_videos = sorted(persons_videos, key=lambda person: (person['title'].lower()))
    for video_data in sorted_persons_videos:
        # print(video_data)
        markup = await get_inline_goto_person_markup(video_data['_id'])
        result_id = hashlib.md5(video_data['_id'].encode()).hexdigest()
        result = InlineQueryResultAudio(
            id=result_id,
            audio_url=video_data['tg_audio_id'],
            title=video_data['title'],
            caption=f'В чем сила?\n\n<tg-spoiler>{video_data['thesis']}</tg-spoiler>',
            reply_markup=markup
        )
        search_results.append(result)

    await bot.answer_inline_query(
        query.id,
        results=search_results[:50],
        cache_time=300,
    )
