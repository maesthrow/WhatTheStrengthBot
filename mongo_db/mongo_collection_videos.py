from datetime import datetime

from pytube import YouTube

from mongo_db.mongo import db


async def get_videos_collection():
    videos_collection = db["videos"]
    return videos_collection


async def add_video(tg_audio_id: str, tg_preview_id: str, text, thesis, yt: YouTube = None, video_info: dict = None):
    """Добавляет данные о видео в коллекцию videos, где ключ - video_id видео с YouTube."""
    videos_collection = db["videos"]  # Получаем коллекцию "videos" из базы данных

    if yt:
        video_id = yt.video_id
        title = yt.title
        publish_date = yt.publish_date
    elif video_info:
        video_id = video_info.get('id')
        title = video_info.get('title')
        publish_date = datetime.strptime(video_info.get('upload_date'), '%Y%m%d')
    else:
        raise ValueError("Отсутствуют данные для извлечения информации о видео.")

    # Проверяем, существует ли документ для данного видео в базе данных
    video_document = videos_collection.find_one({"_id": video_id})

    if video_document:
        return

    # Создаем структуру документа видео
    video_document = {
            "_id": video_id,
            "title": title,
            "tg_audio_id": tg_audio_id,
            "tg_preview_id": tg_preview_id,
            "text": text,
            "thesis": thesis,
            "views": 1,
            "likes": 0,
            "dislikes": 0,
            "publish_date": publish_date
        }

    try:
        print(f"Добавление видео {video_id} в коллекцию videos в базе данных:")
        videos_collection.insert_one(video_document)
        print("Успешно")
    except Exception as e:
        print(f"Ошибка при добавлении видео {video_id} в коллекцию videos в базу данных:", e)


async def set_video_data(video_id, data):
    """Обновляет данные видео."""
    videos_collection = db["videos"]
    videos_collection.update_one({"_id": video_id}, {"$set": data})


async def set_video_additional_default_data():
    """Обновляет данные видео, добавляя отсутствующие поля со значениями по умолчанию."""
    videos_collection = db["videos"]

    # Установка значений по умолчанию для всех документов, у которых отсутствуют эти поля
    default_values = {"views": 1, "likes": 0, "dislikes": 0}

    # Проходим по каждому документу и добавляем отсутствующие значения
    for field, value in default_values.items():
        # Используем $set и $exists для проверки и установки значений
        videos_collection.update_many({field: {"$exists": False}}, {"$set": {field: value}})


async def get_video_data(video_id: str):
    """Возвращает данные видео по его идентификатору из коллекции videos в базе данных."""
    videos_collection = db["videos"]
    video_document = videos_collection.find_one({"_id": video_id})
    return video_document
