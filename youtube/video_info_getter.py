import os

from googleapiclient.discovery import build

from youtube.video_id_getter import extract_video_id

API_KEY = os.getenv('YOU_TUBE_DATA_API_KEY')

youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_video_description(url):
    video_id = extract_video_id(url)

    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    if video_response['items']:
        return video_response['items'][0]['snippet']['description']
    else:
        return "No description available or video not found."





