import io
import requests
from pydub import AudioSegment
from load_all import bot
from salute_speech.audio_to_text import download_file
from salute_speech.auth import get_access_token

RECOGNITION_URL = 'https://smartspeech.sber.ru/rest/v1/speech:recognize'


async def get_text_from_audio(audio_file_id):
    try:
        token = await get_access_token()
        if not token:
            print("Ошибка аутентификации. Пожалуйста, попробуйте позже.")
            return

        file = await download_file(audio_file_id)
        audio_segments = split_audio(file)
        print(len(audio_segments))

        full_text = []
        for segment in audio_segments:
            pcm_data = get_audio_pcm_format(segment)
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'audio/x-pcm;bit=16;rate=16000'
            }
            response = requests.post(RECOGNITION_URL, headers=headers, data=pcm_data, verify=False)
            #print(f'result {response.content}')
            if response.status_code == 200:
                result = response.json().get('result', [])
                if result:
                    print(f'result {result}')
                    full_text.append(' '.join(result))

        return ' '.join(full_text)

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


def split_audio(file):
    audio = AudioSegment.from_file(file)
    duration = len(audio)
    segments = []
    for start in range(0, duration, 58000):  # 60000ms = 60s
        end = min(start + 58000, duration)
        segment = audio[max(0, start - 1000):end]
        segments.append(segment)
    return segments


def get_audio_pcm_format(audio):
    audio = audio.set_frame_rate(16000).set_sample_width(2).set_channels(1)
    pcm_data = io.BytesIO()
    audio.export(pcm_data, format="raw")
    pcm_data = pcm_data.getvalue()
    return pcm_data
