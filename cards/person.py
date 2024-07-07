from datetime import datetime

from pytube import YouTube

from data.users_repository import get_user_likes
from load_all import bot
from mongo_db.mongo_collection_videos import get_video_data, set_video_data
from utils.buttons import get_person_video_card_keyboard
from utils.text import get_thesis_caption
from utils.user import get_like_icon_for_post
from youtube.pytube_lib import get_yt_by_id
from youtube.yt_dlp_lib import get_video_info_by_id


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
            yt = get_yt_by_id(video_id)
            # video_info = get_video_info_by_id(video_id)
            if not preview_file_id:
                photo_message = await bot.send_photo(
                    chat_id,
                    # photo=video_info.get('thumbnail'),
                    photo=yt.thumbnail_url,
                    caption=get_thesis_caption(thesis),
                    reply_markup=markup,
                )
                video_data["tg_preview_id"] = photo_message.photo[0].file_id

            # video_data["publish_date"] = datetime.strptime(video_info.get('upload_date'), '%Y%m%d')
            video_data["publish_date"] = yt.publish_date
            await bot.send_message(chat_id=chat_id, text=f'upload_date {video_data["publish_date"]}')
            await set_video_data(video_id, video_data)

        await bot.send_audio(chat_id=chat_id, audio=audio_file_id)

