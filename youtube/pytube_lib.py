from pytube import YouTube

from youtube.video_attributes_getter import get_video_url


def get_yt_by_id(video_id: str):
    return get_yt_by_url(get_video_url(video_id))


def get_yt_by_url(video_url: str):
    return YouTube(url=video_url, use_oauth=False, allow_oauth_cache=True)
