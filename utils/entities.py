import re

from mongo_db.mongo_collection_videos import get_videos_collection
from utils.number_visualizer import view_int


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
    return entities


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
        result = re.sub(r'сила', '', result).strip()  # Замена "сила" на ""
        result = re.sub(r'\sи\s', ', ', result).strip()  # Замена " и " на ", "
        result = re.sub(r'^в\s', '', result).strip()  # Замена "в " на "" в начале текста
        result = re.sub(r',\sв\s', ', ', result).strip()  # Замена ",в " на ""
        result = re.sub(r'балабанове', 'Балабанове', result).strip()
        result = re.sub(r'боге', 'Боге', result).strip()
        results.append(result.strip())
    for result in results:
        for entity in re.split(r',\s(?!но)', result):
            s.add(entity)
    # Формирование кортежа результатов
    return s


async def get_entities_statistic() -> list:
    entities = await load_entities()
    sorted_entities = sorted(entities.items(), key=lambda item: item[1], reverse=True)

    # Создание словаря для хранения результатов
    result_dict = {}

    # Наполнение словаря
    for text, number in sorted_entities:
        if not result_dict.get(number):
            result_dict[number] = []
        result_dict[number].append(text)

    # Формирование итогового словаря с объединением строк, разделенных точкой с запятой
    final_dict = {view_int(k): '\n'.join(sorted([e.capitalize() for e in v])) for k, v in result_dict.items()}

    result = []
    # Вывод результата
    for key, value in final_dict.items():
        result.append(f"{key}\n{value}\n")
    return result


