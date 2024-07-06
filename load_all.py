import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Router
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from langchain_community.chat_models import GigaChat
from wit import Wit


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

WIT_AI_TOKEN = os.getenv('WIT_AI_TOKEN')

GIGA_AUTH_DATA = os.getenv("GIGA_AUTH_DATA")

# Авторизация в сервисе GigaChat
giga_chat = GigaChat(credentials=GIGA_AUTH_DATA, verify_ssl_certs=False)


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

storage = MemoryStorage()

bot = Bot(token=str(BOT_TOKEN), parse_mode="HTML")
dp = Dispatcher(bot=bot, storage=storage)
wit_client = Wit(WIT_AI_TOKEN)


async def setup_bot():
    pass

