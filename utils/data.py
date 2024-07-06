import datetime

from mongo_db.mongo_collection_videos import get_videos_collection, set_video_data, get_video_data


async def remove_publish_dates():
    videos = await get_videos_collection()
    for video in videos.find():
        video_data = video
        video_data['publish_date'] = datetime.date.min
        await set_video_data(video['_id'], video_data)
