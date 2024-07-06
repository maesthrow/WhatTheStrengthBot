import datetime
import time

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
        if not preview_file_id or True:
            yt = get_youtube_instance(video_id)
            print(f'yt.video_id {yt.video_id}')
            print(f'yt.publish_date {yt.publish_date}')
            if not preview_file_id:
                photo_message = await bot.send_photo(
                    chat_id,
                    photo=yt.thumbnail_url,
                    caption=get_thesis_caption(thesis),
                    reply_markup=markup,
                )
                video_data["tg_preview_id"] = photo_message.photo[0].file_id

            video_data["publish_date"] = yt.publish_date
            await bot.send_message(chat_id=chat_id, text=f'yt.publish_date {yt.publish_date}\nyt.title {yt.title}')
            await set_video_data(video_id, video_data)

        await bot.send_audio(chat_id=chat_id, audio=audio_file_id)


def get_youtube_instance(video_id):
    base_url = "https://www.youtube.com/watch?v="
    video_url = base_url + video_id
    yt = retry_access_ty_object(video_url)
    return yt


def retry_access_ty_object(url, max_retries=5, interval_secs=5, on_progress_callback=None):
    """
    Retries creating a YouTube object with the given URL and accessing its title several times
    with a given interval in seconds, until it succeeds or the maximum number of attempts is reached.
    If the object still cannot be created or the title cannot be accessed after the maximum number
    of attempts, the last exception is raised.
    """
    last_exception = None
    for i in range(max_retries):
        try:
            yt = YouTube(url, on_progress_callback=on_progress_callback)
            title = yt.title  # Access the title of the YouTube object.
            return yt  # Return the YouTube object if successful.
        except Exception as err:
            last_exception = err  # Keep track of the last exception raised.
            print(f"Failed to create YouTube object or access title. Retrying... ({i+1}/{max_retries})")
            time.sleep(interval_secs)  # Wait for the specified interval before retrying.