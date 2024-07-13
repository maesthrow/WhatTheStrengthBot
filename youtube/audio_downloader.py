import os
import re

from moviepy.audio.io.AudioFileClip import AudioFileClip
from mutagen.id3 import ID3, TIT2, TPE1
from mutagen.mp3 import MP3
from pydub import AudioSegment
from pytube import YouTube
from youtube_dl.utils import sanitize_filename

from utils.filename import get_splitter
from youtube.sections_time_getter import extract_sections
from youtube.youtube_api_video_info_getter import get_video_attribute
from youtube.yt_dlp_lib import get_video_info_by_url
from yt_dlp import YoutubeDL

TEMP_FOLDER = 'temp\\origin_audio'
TEMP_FOLDER_STRENGTHS = 'temp\\strengths'


def download_audio_pytube(youtube_url, new_filename: str, author: str = None):
    try:
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_path = audio_stream.download(output_path=TEMP_FOLDER_STRENGTHS)
        print(audio_stream.default_filename)

        if new_filename:
            new_filepath_mp4 = os.path.join(TEMP_FOLDER_STRENGTHS, new_filename + ".mp4")
            new_filepath_mp3 = os.path.join(TEMP_FOLDER_STRENGTHS, new_filename + ".mp3")

            os.rename(audio_path, new_filepath_mp4)

            # Конвертация MP4 в MP3
            audio = AudioSegment.from_file(new_filepath_mp4, format="mp4")
            audio.export(new_filepath_mp3, format="mp3")

            # Добавление тегов
            audio_file = MP3(new_filepath_mp3, ID3=ID3)
            audio_file.tags.add(TIT2(encoding=3, text=new_filename))
            if author:
                audio_file.tags.add(TPE1(encoding=3, text=author))
            else:
                audio_file.tags.add(TPE1(encoding=3, text=yt.author))
            audio_file.save()

            # Опционально удалить оригинальный аудиофайл
            os.remove(new_filepath_mp4)

            print(new_filepath_mp3)
            return new_filepath_mp3

        return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


def download_audio_section_pytube(youtube_url, section_name):
    times = _get_const_times(youtube_url)
    if not times:
        yt = YouTube(youtube_url)
        description = get_video_attribute(youtube_url, 'description')
        times = extract_sections(description, yt.length)
    print(f'times {times}')
    if times and section_name in times.keys():
        start_time, end_time = times[section_name]
        return _download_audio_section_pytube(youtube_url, start_time, end_time, section_name)

    return None


def _download_audio_section_pytube(youtube_url, start_time, end_time, section_name):
    yt = YouTube(youtube_url)
    audio = yt.streams.filter(only_audio=True).first()
    temp_file_path = os.path.join(TEMP_FOLDER_STRENGTHS, audio.default_filename)
    audio.download(output_path=TEMP_FOLDER_STRENGTHS)

    # Обрезать аудио
    splitter = get_splitter(audio.default_filename)
    file_name = f"{audio.default_filename.split(splitter)[0].strip()} - {sanitize_filename(section_name)}"

    final_audio_path = (os.path.join(TEMP_FOLDER_STRENGTHS, f'{file_name}.mp3'))
    with AudioFileClip(temp_file_path) as audio_clip:
        trimmed_audio = trim_audio(audio_clip, start_time, end_time)
        try:
            trimmed_audio.write_audiofile(final_audio_path, codec='libmp3lame')  # Ensure using correct codec
        except Exception as e:
            print(f"Failed to write audio file: {e}")

    # Добавление метаданных к файлу
    audio = MP3(final_audio_path, ID3=ID3)
    audio.tags.add(TIT2(encoding=3, text=file_name))
    audio.save()

    # Опционально удалить оригинальный аудиофайл
    os.remove(temp_file_path)

    return final_audio_path


def download_audio_yt_dlp(youtube_url, new_filename: str, author: str = None):
    try:
        ydl_opts = {
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(TEMP_FOLDER_STRENGTHS, f"{new_filename}.%(ext)s"),
            'quiet': False
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            audio_file_path = ydl.prepare_filename(info_dict)

        # Добавление тегов
        audio_file = MP3(audio_file_path, ID3=ID3)
        audio_file.tags.add(TIT2(encoding=3, text=new_filename))
        if author:
            audio_file.tags.add(TPE1(encoding=3, text=author))
        else:
            audio_file.tags.add(TPE1(encoding=3, text=info_dict.get('uploader', 'Unknown artist')))
        audio_file.save()

        print(audio_file_path)
        return audio_file_path

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


def download_audio_section_yt_dlp(youtube_url, section_name):
    times = _get_const_times(youtube_url)
    if not times:
        video_info = get_video_info_by_url(youtube_url)
        description = video_info.get('description')
        duration = video_info.get('duration')
        times = extract_sections(description, duration)
    if times and section_name in times.keys():
        start_time, end_time = times[section_name]
        return _download_audio_section_yt_dlp(youtube_url, start_time, end_time, section_name)

    return None


def _download_audio_section_yt_dlp(youtube_url, start_time, end_time, section_name):
    ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(TEMP_FOLDER_STRENGTHS, '%(id)s.%(ext)s')
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            temp_file_path = os.path.join(TEMP_FOLDER_STRENGTHS, f"{info_dict['id']}.mp3")

        # file_base = os.path.splitext(os.path.basename(temp_file_path))[0]
        splitter = get_splitter(info_dict.get('title'))
        person_name = info_dict.get('title').split(splitter)[0].strip()
        file_name = f"{person_name} - {sanitize_filename(section_name)}"
        # file_name = f"Солодников - В чем сила"
        final_audio_path = os.path.join(TEMP_FOLDER_STRENGTHS, f'{file_name}.mp3')

        with AudioFileClip(temp_file_path) as audio_clip:
            trimmed_audio = trim_audio(audio_clip, start_time, end_time)
            trimmed_audio.write_audiofile(final_audio_path, codec='libmp3lame')

        audio = MP3(final_audio_path, ID3=ID3)
        audio.tags.add(TIT2(encoding=3, text=file_name))
        audio.tags.add(TPE1(encoding=3, text=info_dict.get('uploader', 'Unknown')))
        audio.save()

        return final_audio_path
    except Exception as e:
        print(f"Failed to process audio: {e}")
        return None
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def _get_const_times(youtube_url) -> dict:
    if youtube_url == 'https://youtu.be/CWX0sALDP54?si=ZcYz_Wai-11UHmBD':  # Егор Крид
        return {'В чем сила?': ('1:49:03.00', '1:49:23.00')}
    if youtube_url == 'https://youtu.be/glbSMlBhY30?si=xoSbeHjugkmjxFXQ':  # Балагов
        return {'В чем сила?': ('1:12:03.00', '1:12:17.00')}
    if youtube_url == 'https://youtu.be/I74CLwzAnwA?si=T81U7FoMDPhyIZLr':  # ГРОТ (проблем аограничения по возрасту pytube.exceptions.AgeRestrictedError: I74CLwzAnwA is age restricted, and can't be accessed without logging in.)
        return {'В чем сила?': ('1:05:21.00', '1:07:08.00')}
    if youtube_url == 'https://youtu.be/Bj7q5VAf8-w?si=feOPV23JhQFKuOzx':  # Гуриев
        return {'В чем сила?': ('1:12:30.00', '1:12:58.00')}
    if youtube_url == 'https://youtu.be/uMR9gTPhVHo?si=MAvOH3TF5GlqNjQJ':  # Нурлан Сабуров
        return {'В чем сила?': ('1:06:22.00', '1:06:40.00')}
    if youtube_url == 'https://youtu.be/WjqBS5TI2YE?si=XWc2KIe_ZLdVa56S':  # Порнофильмы (проблем аограничения по возрасту pytube.exceptions.AgeRestrictedError: I74CLwzAnwA is age restricted, and can't be accessed without logging in.)
        return {'В чем сила?': ('1:12:09.00', '1:13:01.00')}
    if youtube_url == 'https://youtu.be/zl7FAusDuAY?si=6LEoW1XBzEJ852uK':  # Бекмамбетов
        return {'В чем сила?': ('1:25:34.00', '1:25:45.00')}
    if youtube_url == 'https://youtu.be/jcu581GBmPs?si=an1O-4R72vGjm0zl':  # Батыгин
        return {'В чем сила?': ('1:19:15.00', '1:19:24.50')}
    if youtube_url == 'https://youtu.be/mZjOHXZuRPM?si=puOgMeYeVg0mOQ37':  # Долгополов
        return {'В чем сила?': ('1:20:38.00', '1:20:57.00')}
    if youtube_url == 'https://youtu.be/i-v3f-3lbdU?si=nhz0FOurh9s_rCZu':  # Бардаш
        return {'В чем сила?': ('2:13:18.00', '2:13:29.00')}
    if youtube_url == 'https://youtu.be/x-N2PmMGfnI?si=IOfW8zcCLvLsSE8Z':  # Щербаков
        return {'В чем сила?': ('1:35:36.00', '1:36:32.00')}
    if youtube_url == 'https://youtu.be/aiOcgApMVcY?si=HdDBJLtUlXwGqJD9':  # Андрей Колесников
        return {'В чем сила?': ('1:17:06.00', '1:17:18.00')}
    if youtube_url == 'https://youtu.be/Uzu9clzaLvg?si=K49WOMC5GZhltOoJ':  # Лапенко
        return {'В чем сила?': ('1:14:24.00', '1:14:50.00')}
    if youtube_url == 'https://youtu.be/kE04ATMQyso?si=e3C4bDo1pfhOjwxN':  # Anacondaz
        return {'В чем сила?': ('1:16:03.00', '1:17:27.00')}
    if youtube_url == 'https://youtu.be/sRwXMnLgcK4?si=pKZXEDL_Ez7ymRYt':  # Горбачева
        return {'В чем сила?': ('1:39:05.00', '1:39:49.00')}
    if youtube_url == 'https://youtu.be/95ReakCrKX0?si=9Ai4D_G2eKgg_L1y':  # IC3PEAK
        return {'В чем сила?': ('1:30:12.00', '1:30:36.00')}
    if youtube_url == 'https://youtu.be/PWt27h_scaY?si=SKBGXiH_2--Q5O-M':  # Лошак
        return {'В чем сила?': ('1:45:56.00', '1:47:05.00')}
    if youtube_url == 'https://youtu.be/XnHIsoonXHc?si=4NKLP-8IBE3yL6bH':  # Усович
        return {'В чем сила?': ('1:14:05.00', '1:14:23.00')}
    if youtube_url == 'https://youtu.be/skFNJ3tB67M?si=2WTrk5TIntouhtLM':  # Козырев
        return {'В чем сила?': ('1:50:13.00', '1:50:36.00')}
    if youtube_url == 'https://youtu.be/xH777TiUF90?si=-NReNmfX_aACqPHM':  # Юра Борисов
        return {'В чем сила?': ('1:19:03.00', '1:19:36.00')}
    if youtube_url == 'https://youtu.be/JB7E8wuEHjI?si=J2Ht5MbWMt3c80WY':  # Усачев
        return {'В чем сила?': ('1:40:07.00', '1:40:32.00')}
    if youtube_url == 'https://youtu.be/Ed47sWpgvf0?si=mn6cDS3L2qRYw93m':  # Бодров
        return {'В чем сила?': ('0:01:46.00', '0:2:40.00')}
    if youtube_url == 'https://youtu.be/mh-7jvePXF4?si=w3B7GHSd-QVBiO8d':  # Солодников
        return {'В чем сила?': ('2:41:44.00', '2:41:49.00')}

    if youtube_url == 'https://youtu.be/KUVt2zXRb6Y?si=KZWC3elkQadloqxV':  # Алик Авганец
        return {'В чем сила?': ('0:00:25.00', '0:01:53.00')}

    if youtube_url == 'https://youtu.be/en6ZUDjvUEs?si=pxMlkEuYnKbEUz7D':  # Сергей Бодров
        return {'В чем сила?': ('0:01:46.00', '0:3:23.30')}


    # ? - Сигарев, Павлов-Андреев, Ланьков

    return {}


def time_str_to_seconds(t_str):
    """ Конвертирует строку времени 'HH:MM:SS' или 'HH:MM:SS.00' в секунды. """
    parts = re.split('[:.]', t_str)
    h, m, s = map(float, parts[:3])
    return h * 3600 + m * 60 + s


def seconds_to_time_str(seconds):
    """ Конвертирует секунды обратно в строку времени 'HH:MM:SS.00'. """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.00"


def trim_audio(audio_clip, start_time_str, end_time_str):
    clip_duration = audio_clip.duration

    # Преобразуем строковые значения времени в секунды
    start_time = time_str_to_seconds(start_time_str)
    end_time = time_str_to_seconds(end_time_str)

    # Проверяем и корректируем end_time, если он выходит за пределы длительности аудиоклипа
    if end_time > clip_duration:
        end_time = clip_duration

    # Обрезаем аудио
    trimmed_audio = audio_clip.subclip(start_time, end_time)

    # Возвращаем конечное время в строковом формате для отображения или использования
    end_time_str = seconds_to_time_str(end_time)
    print(f"Trimmed audio ends at {end_time_str}")  # Отображаем обновленное конечное время

    return trimmed_audio
