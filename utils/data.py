from mongo_db.mongo_collection_videos import get_videos_collection, set_video_data, get_video_data


async def remove_publish_dates():
    videos = await get_videos_collection()
    for video in videos:
        video_data = await get_video_data(video['_id'])
        video_data['publish_date'] = None
        await set_video_data(video['_id'], video_data)
