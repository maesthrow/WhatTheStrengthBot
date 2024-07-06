import datetime

from aiogram.enums import ParseMode
from pytube import YouTube

from data.users_repository import get_user_likes
from load_all import bot
from mongo_db.mongo_collection_videos import get_video_data, set_video_data
from utils.buttons import get_person_video_card_keyboard
from utils.text import get_thesis_caption
from utils.user import get_like_icon_for_post


async def send_video_card(chat_id, video_id):
    video_data = await get_video_data(video_id)
    if video_data:
        audio_file_id = video_data.get('tg_audio_id')
        preview_file_id = video_data.get('tg_preview_id')
        publish_date = video_data.get('publish_date')
        text = video_data.get('text')
        thesis = video_data.get('thesis')
        like_icon = get_like_icon_for_post(video_id, await get_user_likes(chat_id))
        markup = get_person_video_card_keyboard(video_id, like_icon, video_data['likes'])

        if preview_file_id:
            await bot.send_photo(
                chat_id,
                photo=preview_file_id,
                caption=get_thesis_caption(thesis),
                reply_markup=markup),
        if not preview_file_id or publish_date == datetime.date.min:
            yt = get_youtube_instance(video_id)
            if not preview_file_id:
                photo_message = await bot.send_photo(
                    chat_id,
                    photo=yt.thumbnail_url,
                    caption=get_thesis_caption(thesis),
                    reply_markup=markup,
                )
                video_data["tg_preview_id"] = photo_message.photo[0].file_id

            if publish_date == datetime.date.min:
                video_data["publish_date"] = yt.publish_date

            await set_video_data(video_id, video_data)

        await bot.send_audio(chat_id=chat_id, audio=audio_file_id)


def get_youtube_instance(video_id):
    base_url = "https://www.youtube.com/watch?v="
    video_url = base_url + video_id
    yt = YouTube(video_url)
    return yt
