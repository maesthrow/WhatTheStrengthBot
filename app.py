import asyncio

from aiogram.methods import DeleteWebhook
from aiogram_dialog import setup_dialogs

from dialogs.main_menu.windows import dialog_main_menu
from dialogs.persons.windows import dialog_persons
from load_all import bot, dp
from mongo_db.mongo import close_mongo_client


async def on_shutdown():
    await close_mongo_client()
    await bot.close()


async def on_startup():
    pass
    #await setup_bot()


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot, on_shutdown=on_shutdown, on_startup=on_startup)


if __name__ == '__main__':
    import handlers_pack.handlers_command
    import handlers_pack.handlers_text
    import handlers_pack.handlers_voice
    import handlers_pack.handlers_buttons
    import handlers_pack.handlers_inline_query

    dp.include_router(dialog_persons)
    dp.include_router(dialog_main_menu)

    setup_dialogs(dp)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот был остановлен вручную')


# start - 🚀️ поехали
# select - 👥 выбор персон
# search - 🔍️ поиск персон
# playlist - 🎧 плейлисты ответов
# contact - 👨‍💻 написать разработчику
# help - ❔ помощь

