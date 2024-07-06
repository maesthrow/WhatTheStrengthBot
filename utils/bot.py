import asyncio
from typing import List

from aiogram.utils.media_group import MediaGroupBuilder

from load_all import bot


async def get_bot_link():
    bot_info = await bot.get_me()
    username = bot_info.username
    bot_link = f"https://t.me/{username}"
    return bot_link


async def get_bot_name():
    bot_info = await bot.get_me()
    name = bot_info.first_name
    return name


async def send_media_group(chat_id, media_group_builders: List[MediaGroupBuilder]):
    for mg_builder in media_group_builders:
        await bot.send_chat_action(chat_id, "typing")
        media_group = mg_builder.build()
        if len(media_group) > 0:
            await bot.send_media_group(chat_id=chat_id, media=media_group)
            await asyncio.sleep(0.3)
