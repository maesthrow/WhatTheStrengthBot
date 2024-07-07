import os
import re

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from pytube import YouTube

from data.users_repository import get_user_likes
from giga_chat.giga import giga_get_thesis, giga_get_edit_text
from load_all import dp, bot
from mongo_db.mongo_collection_videos import add_video, get_video_data, set_video_data
from salute_speech.audio_to_text_pro import get_text_from_audio
from utils.buttons import get_person_video_card_keyboard
from utils.text import get_redacted_text, get_caption, check_censored, get_thesis_caption
from utils.user import get_like_icon_for_post, EMPTY_LIKE_ICON
from youtube.audio_downloader import download_audio_yt_dlp, download_audio_section_yt_dlp
from youtube.video_info_getter import get_video_description
from youtube.yt_dlp_lib import get_video_info_by_url

router = Router()
dp.include_router(router)


@router.message(F.text & (F.text.contains("youtube.com") | F.text.contains("youtu.be")))
async def text_youtube_link_handler(message: Message):
    await bot.send_chat_action(message.chat.id, "typing")
    # Извлекаем URL-адрес YouTube из сообщения
    youtube_urls = re.findall(r'(https?://[^\s]+)', message.text)

    for url in youtube_urls:
        video_info = get_video_info_by_url(url)
        print(f'info {video_info.get('thumbnail')}')

        # yt = retry_access_ty_object(url)
        preview_url = video_info.get('thumbnail')

        video_data = await get_video_data(video_info.get('id'))
        if not video_data:
            wait_message = await bot.send_message(message.chat.id, 'Минуту, сейчас узнаем в чем сила...')
            await bot.send_chat_action(message.chat.id, "typing")

            if url == 'https://youtu.be/fz6lGsgEGZ8?si=kJM1FK4dEff9LXfW':
                audio_file_path = download_audio_yt_dlp(url, 'Данила Багров - В чем сила', 'Брат-2')
            elif url == 'https://youtu.be/woABg3bbh0g?si=taddQVW4c5Nd3lgE':
                audio_file_path = download_audio_yt_dlp(url, 'Сергей Бодров - В чем сила', 'Сергей Бодров')
            else:
                audio_file_path = download_audio_section_yt_dlp(url, 'В чем сила?')

            await bot.delete_message(wait_message.chat.id, wait_message.message_id)

            if not audio_file_path:
                await bot.send_message(message.chat.id, 'Не удалось узнать в чем сила')
                return

            photo_message = await bot.send_photo(message.chat.id, photo=preview_url)
            photo_file_id = photo_message.photo[0].file_id

            current_directory = os.getcwd()
            full_audio_file_path = rf'{os.path.join(current_directory, audio_file_path)}'

            audio_file = FSInputFile(full_audio_file_path)
            audio_message = await bot.send_audio(chat_id=message.chat.id, audio=audio_file)
            audio_file_id = audio_message.audio.file_id

            await bot.send_chat_action(message.chat.id, "typing")

            text = await get_redacted_text(audio_file_id)
            thesis = giga_get_thesis(check_censored(text))

            await add_video(video_info, audio_file_id, photo_file_id, text, thesis)

            markup = get_person_video_card_keyboard(video_info.get('id'), EMPTY_LIKE_ICON, 0)
            await bot.edit_message_caption(
                chat_id=photo_message.chat.id,
                message_id=photo_message.message_id,
                caption=get_thesis_caption(thesis),
                reply_markup=markup
            )
            os.remove(full_audio_file_path)  # Удаление файла после отправки, чтобы освободить место на диске

        if video_data:
            audio_file_id = video_data.get('tg_audio_id')
            preview_file_id = video_data.get('tg_preview_id')
            text = video_data.get('text')
            thesis = video_data.get('thesis')
            like_icon = get_like_icon_for_post(video_info.get('id'), await get_user_likes(message.from_user.id))
            markup = get_person_video_card_keyboard(video_info.get('id'), like_icon, video_data['likes'])

            if preview_file_id:
                await bot.send_photo(
                    message.chat.id, photo=preview_file_id, caption=get_thesis_caption(thesis), reply_markup=markup
                )
            else:
                photo_message = await bot.send_photo(
                    message.chat.id, photo=preview_url, caption=get_thesis_caption(thesis), reply_markup=markup
                )
                video_data["tg_preview_id"] = photo_message.photo[0].file_id
                await set_video_data(video_info.get('id'), video_data)

            await bot.send_audio(chat_id=message.chat.id, audio=audio_file_id)




# async def _send_text(message, audio_file_id):
#     text = await get_text_from_audio(audio_file_id)
#     if text:
#         await bot.send_message(message.chat.id, text)
#
#
# async def _send_thesis(message, audio_file_id):
#     text = await get_text_from_audio(audio_file_id)
#     thesis = giga_get_thesis(text)
#     if thesis:
#         await bot.send_message(message.chat.id, thesis)
