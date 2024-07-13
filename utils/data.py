import datetime

from mongo_db.mongo_collection_videos import get_videos_collection, set_video_data, get_video_data


async def remove_publish_dates():
    videos = await get_videos_collection()
    for video in videos.find():
        video_data = video
        video_data['publish_date'] = datetime.datetime.min
        await set_video_data(video['_id'], video_data)


async def reset_publish_dates_to_str():
    videos = await get_videos_collection()
    for video in videos.find():
        video_data = video
        date_formats = [
            "%Y-%m-%dT%H:%M:%SZ",         # Формат без миллисекунд и часового пояса
            "%Y-%m-%dT%H:%M:%S.%fZ",       # Формат с миллисекундами
            "%Y-%m-%dT%H:%M:%S.%f%z"       # Формат с миллисекундами и часовым поясом
        ]
        original_date = video_data['publish_date']
        for date_format in date_formats:
            try:
                # Пробуем преобразовать строку в datetime по каждому из форматов
                if isinstance(original_date, str):
                    video_data['publish_date'] = datetime.datetime.strptime(original_date, date_format)
                # Если дата уже в формате datetime, форматируем её сразу
                video_data['publish_date'] = video_data['publish_date'].strftime("%Y-%m-%dT%H:%M:%SZ")
                break  # Прерываем цикл, если преобразование успешно
            except ValueError:
                continue  # Продолжаем попытки с другим форматом
        else:
            # Если ни один формат не подошёл, выводим сообщение об ошибке
            print(f"Не удалось обработать дату для видео {video['_id']} с датой {original_date}")
            continue

        # Сохраняем обновлённые данные видео
        await set_video_data(video['_id'], video_data)
