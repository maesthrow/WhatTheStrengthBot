import os

from moviepy.audio.io.AudioFileClip import AudioFileClip
from mutagen.id3 import ID3, TIT2, TPE1
from mutagen.mp3 import MP3
from pydub import AudioSegment
from pytube import YouTube
from youtube_dl.utils import sanitize_filename

from utils.filename import get_splitter
from youtube.sections_time_getter import extract_sections
from youtube.video_info_getter import get_video_description

TEMP_FOLDER = 'temp\\origin_audio'
TEMP_FOLDER_STRENGTHS = 'temp\\strengths'


def download_audio(youtube_url, new_filename: str, author: str = None):
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


def download_audio_section(youtube_url, section_name):
    times = _get_const_times(youtube_url)
    if not times:
        yt = YouTube(youtube_url)
        description = get_video_description(youtube_url)
        times = extract_sections(description, yt)
    print(f'times {times}')
    if times and section_name in times.keys():
        start_time, end_time = times[section_name]
        return _download_audio_section(youtube_url, start_time, end_time, section_name)

    return None


def _download_audio_section(youtube_url, start_time, end_time, section_name):
    yt = YouTube(youtube_url)
    audio = yt.streams.filter(only_audio=True).first()
    temp_file_path = os.path.join(TEMP_FOLDER_STRENGTHS, audio.default_filename)
    audio.download(output_path=TEMP_FOLDER_STRENGTHS)

    # Обрезать аудио
    splitter = get_splitter(audio.default_filename)
    file_name = f"{audio.default_filename.split(splitter)[0].strip()} - {sanitize_filename(section_name)}"

    final_audio_path = (os.path.join(TEMP_FOLDER_STRENGTHS, f'{file_name}.mp3'))
    with AudioFileClip(temp_file_path) as audio_clip:
        trimmed_audio = audio_clip.subclip(start_time, end_time)
        try:
            trimmed_audio.write_audiofile(final_audio_path, codec='libmp3lame')  # Ensure using correct codec
        except Exception as e:
            print(f"Failed to write audio file: {e}")

    # Добавление метаданных к файлу
    audio = MP3(final_audio_path, ID3=ID3)
    audio.tags.add(TIT2(encoding=3, text=file_name))
    audio.tags.add(TPE1(encoding=3, text=yt.author))
    audio.save()

    # Опционально удалить оригинальный аудиофайл
    os.remove(temp_file_path)

    return final_audio_path


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
    return {}
