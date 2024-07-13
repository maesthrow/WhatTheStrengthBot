from typing import List

from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder

from data.videos_repository import get_full_playlist
from enums import PlaylistType
from utils.bot import send_media_group


async def send_playlist(message: Message, type_pl: PlaylistType):
    print(type_pl)
    playlist_files = await get_full_playlist()

    if type_pl == PlaylistType.Top10:
        sorted_playlist_files = sorted(
            playlist_files,
            key=lambda audio_file: (-playlist_files[audio_file]['likes'], playlist_files[audio_file]['title']))[:10]
    elif type_pl == PlaylistType.Top20:
        sorted_playlist_files = sorted(
            playlist_files,
            key=lambda audio_file: (-playlist_files[audio_file]['likes'], playlist_files[audio_file]['title']))[:20]
    elif type_pl == PlaylistType.New:
        sorted_playlist_files = sorted(
            playlist_files, key=lambda audio_file: playlist_files[audio_file]['publish_date'], reverse=True)[:10]
    elif type_pl == PlaylistType.Chronology:
        sorted_playlist_files = sorted(
            playlist_files, key=lambda audio_file: playlist_files[audio_file]['publish_date'], reverse=False)
    elif type_pl == PlaylistType.Rating:
        sorted_playlist_files = sorted(
            playlist_files,
            key=lambda audio_file: (-playlist_files[audio_file]['likes'], playlist_files[audio_file]['title']))
    else:
        sorted_playlist_files = []

    print(len(sorted_playlist_files))
    media_group_builders = _get_playlist_builders(sorted_playlist_files)
    await send_media_group(message.chat.id, media_group_builders)


def _get_playlist_builders(playlist: List[str]) -> List[MediaGroupBuilder]:
    builders = [MediaGroupBuilder()]
    for audio_file_id in playlist:
        if len(builders[-1]._media) >= 10:
            builders.append(MediaGroupBuilder())
        builders[-1].add(type='audio', media=audio_file_id)
    return builders
