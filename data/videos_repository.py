import datetime

from aiogram.types import User

from data.users_repository import get_user_likes
from mongo_db.mongo_collection_users import get_user_collection
from mongo_db.mongo_collection_videos import get_videos_collection, get_video_data, set_video_data
from utils.filename import get_splitter
from utils.user import get_like_icon_for_post


async def get_full_playlist() -> dict:
    videos_collection = await get_videos_collection()
    cursor = videos_collection.find()  # Получаем курсор для всех документов в коллекции
    audio_files = {}
    for doc in cursor:
        audio_file_id = doc.get('tg_audio_id')
        if audio_file_id:
            audio_files[audio_file_id] = {
                'title': doc.get('title').split('-')[0].strip(),
                'likes': doc.get('likes'),
                'publish_date': doc.get('publish_date'),
            }
    return audio_files


async def get_persons_videos(tg_user: User):
    videos_collection = await get_videos_collection()
    cursor = videos_collection.find()  # Получаем курсор для всех документов в коллекции
    persons = [doc for doc in cursor]
    return [await _update_title_to_person_select(person, tg_user) for person in persons]


async def set_video_likes(video_id: str, increment: int) -> bool:
    try:
        video_data = await get_video_data(video_id)
        if video_data['likes'] + increment >= 0:
            video_data['likes'] += increment
            await set_video_data(video_id, video_data)
            return True
        return False
    except:
        return False


async def set_video_publish_date(video_id: str, publish_date: datetime) -> bool:
    try:
        video_data = await get_video_data(video_id)
        video_data['publish_date'] = publish_date
        await set_video_data(video_id, video_data)
        return True
    except:
        return False


async def _update_title_to_person_select(person, tg_user: User):
    """Обновляет заголовок видео в словаре."""
    user_likes = await get_user_likes(tg_user.id)
    if 'title' in person: # and ' – ' in person['title']:
        like_icon = get_like_icon_for_post(person['_id'], user_likes)
        splitter = get_splitter(person['title'])
        person['title'] = person['title'].split(f' {splitter} ')[0].replace(' / вДудь', '').strip()
        person['title'] = f'{person['title']} {like_icon} {person['likes']}'
    return person


async def get_search_persons_videos(tg_user: User, query: str):
    videos = await get_persons_videos(tg_user)
    # Отфильтровать видео, у которых 'title' содержит query в любом из слов до разделителя '–'
    filtered_videos = [
        video for video in videos
        if any(word.lower().startswith(query.lower()) for word in video['title'].split('–')[0].split())
    ]
    return filtered_videos
