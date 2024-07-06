from aiogram.types import User

EMPTY_LIKE_ICON = '🤍'
SET_LIKE_ICON = '❤️' #❤️ 💙 🧡


def get_user_full_str(tg_user: User):
    result = str(tg_user.id)
    if tg_user.username:
        result = f'{result} {tg_user.username}'
    result = f'{result} {tg_user.full_name}'
    return result


def get_like_icon_for_post(post_id, user_likes):
    return SET_LIKE_ICON if post_id in user_likes.keys() else EMPTY_LIKE_ICON
