import re


def format_time_stamp(time_str):
    # Функция для форматирования временной метки в строковом формате 'hh:mm:ss.xx'
    parts = time_str.split(':')
    if len(parts) == 3:
        h, m, s = parts
    elif len(parts) == 2:
        h = '0'
        m, s = parts
    elif len(parts) == 1:
        h, m = '0', '0'
        s = parts[0]
    # Добавим поддержку миллисекунд, если они присутствуют
    if '.' in s:
        sec, ms = s.split('.')
        s = f"{sec}.{ms}"
    else:
        s = f"{s}.00"
    return f'{h}:{m}:{s}'


def extract_sections(input_string, video_duration):
    print(f'video_duration {video_duration}')
    pattern = re.compile(r'(\d{1,2}:\d{2}:\d{2}(\.\d+)?|\d{1,2}:\d{2}|\d{1,2})\s+(.*?)\s*(?=\d{1,2}:\d{2}(:\d{2}(\.\d+)?)?\s|$)')
    matches = pattern.findall(input_string)
    sections = {}
    last_end = f"{video_duration // 3600}:{(video_duration % 3600) // 60}:{(video_duration % 60):02}.00"  # Предполагаем, что `yt.length` задано в секундах
    for i in range(len(matches) - 1, -1, -1):
        start_time = format_time_stamp(matches[i][0])
        end_time = last_end
        sections[matches[i][2]] = (start_time, end_time)
        last_end = start_time
    print(f'sections {sections}')
    return sections
