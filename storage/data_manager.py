from aiogram.fsm.storage.base import StorageKey

from load_all import bot, dp


async def get_data(user_id) -> dict:
    storage_key = StorageKey(bot.id, user_id, user_id)
    data = await dp.storage.get_data(storage_key)
    return data


async def set_data(user_id, data: dict):
    storage_key = StorageKey(bot.id, user_id, user_id)
    await dp.storage.update_data(storage_key, data)


async def add_data(user_id, data: dict):
    current_data = await get_data(user_id)
    for key in data.keys():
        current_data[key] = data[key]
    await set_data(user_id, current_data)


async def clear_data(user_id):
    await set_data(user_id, data={})
