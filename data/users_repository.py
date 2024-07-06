from mongo_db.mongo_collection_users import get_user_collection, get_user_data, set_user_data


async def get_user_likes(user_id):
    return await get_user_collection(user_id, 'likes')


async def set_user_likes(user_id, video_id) -> bool:
    try:
        user_data = await get_user_data(user_id)
        if video_id in user_data.get('likes', {}).keys():
            user_data.get('likes', {}).pop(video_id)
        else:
            user_data.get('likes', {})[video_id] = True
        await set_user_data(user_id, user_data)
        return True
    except:
        return False
