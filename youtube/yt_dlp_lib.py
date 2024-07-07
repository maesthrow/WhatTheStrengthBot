from yt_dlp import YoutubeDL

from youtube.video_attributes_getter import get_video_url

ydl_opts = {
    'cookiefile': '/app/youtube/youtube_cookies.txt',
    'quiet': True,
    'noplaylist': True,
    'format': 'bestaudio/best',
    'extract_flat': 'in_playlist'
}


def get_video_info_by_id(video_id: str):
    return get_video_info_by_url(get_video_url(video_id))


def get_video_info_by_url(video_url: str):
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        video_title = info_dict.get('title')
        video_description = info_dict.get('description')
        upload_date = info_dict.get('upload_date')  # Формат YYYYMMDD
        # print(f"Title: {video_title}")
        # print(f"Description: {video_description}")
        # print(f"Upload Date: {upload_date}")
        return info_dict
