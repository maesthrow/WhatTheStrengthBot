import io
import logging
import os
import base64
import requests
from aiogram import Router, F
from aiogram.types import Message

from uuid import uuid4

from pydub import AudioSegment

from load_all import dp
from salute_speech.audio_to_text import get_text_from_audio

# Конфигурация роутера
router = Router()
dp.include_router(router)


@router.message(F.content_type == 'voice')
async def voice_handler(message: Message):
    text = await get_text_from_audio(message.voice.file_id)
    if text:
        await message.answer(text)
    else:
        await message.answer(f"Не удалось распознать текст")





