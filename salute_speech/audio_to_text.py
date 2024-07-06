import io

import requests
from pydub import AudioSegment

from load_all import bot
from salute_speech.auth import get_access_token

RECOGNITION_URL = 'https://smartspeech.sber.ru/rest/v1/speech:recognize'


async def get_text_from_audio(audio_file_id):
    try:
        # Получаем токен доступа
        token = await get_access_token()
        if not token:
            print("Ошибка аутентификации. Пожалуйста, попробуйте позже.")
            return

        # Загружаем аудиофайл
        file = await download_file(audio_file_id)

        # Переводим файл в формат PCM
        pcm_data = get_audio_pcm_format(file)

        # Отправляем файл на распознавание
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'audio/x-pcm;bit=16;rate=16000'
        }
        response = requests.post(RECOGNITION_URL, headers=headers, data=pcm_data, verify=False)
        # Обрабатываем ответ
        if response.status_code == 200:
            result = response.json()['result']
            if result:
                return ' '.join(result)
            else:
                return None
        else:
            print("Ошибка обработки запроса на распознавание.")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


async def download_file(audio_file_id):
    file_info = await bot.get_file(audio_file_id)
    file_path = file_info.file_path
    file = await bot.download_file(file_path)
    return file


def get_audio_pcm_format(file):
    # Преобразуем аудио в PCM формат
    audio = AudioSegment.from_file(file)
    audio = audio.set_frame_rate(16000).set_sample_width(2).set_channels(1)
    pcm_data = io.BytesIO()
    audio.export(pcm_data, format="raw")
    pcm_data = pcm_data.getvalue()
    return pcm_data
