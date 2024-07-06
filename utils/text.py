import re

from giga_chat.giga import giga_get_edit_text
from salute_speech.audio_to_text_pro import get_text_from_audio


INVISIBLE_CHAR = "\u00A0"


async def get_redacted_text(audio_file_id):
    text = await get_text_from_audio(audio_file_id)
    print(f'origin text:\n{text}')
    text = _remove_prefix_up_to_final(text)
    text = (text
            .replace('Юрий', '').replace('юрий', '')
            .replace('Будет дуть', '').replace('будет дуть', '')
            .replace('Дуть будет', '').replace('дуть будет', '')
            .replace('Дуть', '').replace('дуть', '')
            .replace('В чем сила? ', '').replace('в чем сила? ', '')
            .replace('В чем сила, ', '').replace('в чем сила, ', '')
            .replace('В чем сила. ', '').replace('в чем сила. ', '')
            .replace('В чем сила?', '').replace('в чем сила?', '')
            .replace('В чем сила', '').replace('в чем сила', '')
            .replace('\n ', '\n')
            )
    text = _capitalize_first_letter(_clean_text(text))
    edit_text = giga_get_edit_text(check_censored(text))
    if ('Что то в вашем вопросе меня смущает' in edit_text
            or 'Как у нейросетевой языковой модели у меня' in edit_text):
        edit_text = text
    return f'В чем сила?\n{edit_text}.'


def get_caption(text, thesis):
    if ('Что то в вашем вопросе меня смущает' in thesis
            or 'Как у нейросетевой языковой модели у меня' in thesis):
        thesis = ''
    caption = f'{text}\n\n{thesis}'
    if len(caption) > 1000:
        #caption = f'{text.split('\n')[0]}\n{thesis}'
        caption = f'{text[:600]}...\n\n{thesis}'
    return caption.strip()


def get_thesis_caption(thesis):
    if ('Что то в вашем вопросе меня смущает' in thesis
            or 'Как у нейросетевой языковой модели у меня' in thesis):
        thesis = ''
    caption = f'В чем сила?\n\n<tg-spoiler>{thesis}</tg-spoiler>'
    return caption.strip()


def _remove_prefix_up_to_final(text):
    # Удаляем всё до слов "финальная" или "финальное" (в любом регистре), включая само слово
    cleaned_text = re.sub(r"^.*?\b(финальное|финальная)\b", "", text, flags=re.IGNORECASE)
    return cleaned_text.strip()


def _clean_text(text):
    # Удаляем знаки препинания в начале и конце строки, кроме точки в конце
    cleaned_text = re.sub(r"^[^\w]+|[^\w]+$", "", text)
    return cleaned_text


def _capitalize_first_letter(text):
    if text:  # Проверяем, не пуста ли строка
        return text[0].upper() + text[1:]
    return text


def check_censored(text):
    return text.replace('Путин', '').replace('путин', '')


def escape_markdown(text) -> str:
    """Экранирует специальные символы для использования в разметке Markdown V2."""
    if not text:
        return text
    escape_chars = '\\*_[]()<>#+-=|{}.!'
    escaped_text = ''
    can_edit = True
    for char in text:
        if char == '`':
            can_edit = not can_edit
        if char in escape_chars and can_edit:
            escaped_text += '\\' + char
        else:
            escaped_text += char
    return escaped_text