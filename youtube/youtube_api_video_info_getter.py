import os

from googleapiclient.discovery import build

from youtube.video_attributes_getter import extract_video_id

API_KEY = os.getenv('YOU_TUBE_DATA_API_KEY')

youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_video_attribute(url, attribute):
    video_id = extract_video_id(url)

    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    if video_response['items']:
        snippet = video_response['items'][0]['snippet']

        # Особая обработка для получения URL миниатюры
        if attribute == 'thumbnail_url':
            # Предполагаем, что нужна стандартная миниатюра
            return snippet['thumbnails']['default']['url']

        return snippet.get(attribute, f"No {attribute} available for this video.")
    else:
        return f"Video not found."


