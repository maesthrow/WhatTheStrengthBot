import re

from mongo_db.mongo_collection_videos import get_videos_collection


async def load_entities():
    videos = await get_videos_collection()
    for video_data in videos.find():
        thesis = video_data.get('thesis')
        print(f'{thesis} - {get_entities_from_thesis(thesis)}')


def get_entities_from_thesis(text: str) -> tuple:
    # Нормализация текста: удаление точек и перевод в нижний регистр для унификации
    text = text.split('\n')[0].lower().strip('.').strip()

    if 'гость не дал конкретного ответа на вопрос' in text:
        return ()

    # Разделение текста на части, начинающиеся с "в"
    pattern = r'((?:в |сила )[^,.]+(?:, [^,.]+)*(?: и [^,.]+)*)'
    raw_results = re.findall(pattern, text)

    # Обработка результатов: удаление "в " и замена " и " на ", "
    results = []
    for result in raw_results:
        result = re.sub(r'в\s', '', result)  # Замена "в " на ""
        result = re.sub(r'\sи\s', ', ', result)  # Замена " и " на ", "
        result = re.sub(r'сила', '', result)  # Замена "сила" на ""
        results.append(result.strip())

    # Формирование кортежа результатов
    return tuple(results)
