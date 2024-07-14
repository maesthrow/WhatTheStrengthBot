import re

from mongo_db.mongo_collection_videos import get_videos_collection


async def load_entities():
    videos = await get_videos_collection()
    entities = {}
    for video_data in videos.find():
        thesis = video_data.get('thesis')
        # print(f'{thesis} - {get_entities_from_thesis(thesis)}')
        entities_set = get_entities_from_thesis(thesis)
        for entity in entities_set:
            if entity in entities:
                entities[entity] += 1
            else:
                entities[entity] = 1
    print(entities)


def get_entities_from_thesis(text: str) -> set:
    s = set()
    # Нормализация текста: удаление точек и перевод в нижний регистр для унификации
    text = text.split('\n')[0].lower().strip('.').strip()

    if 'гость не дал конкретного ответа на вопрос' in text:
        return set()

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
    for result in results:
        for entity in result.split(', '):
            s.add(entity)
    # Формирование кортежа результатов
    return s
