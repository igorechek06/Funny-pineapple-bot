from bot import dp
from aiogram import types
from src import text


def chat(msg: types.Message):
    return msg.chat.type in ["private"]


@dp.message_handler(lambda msg: chat(msg), commands=["start"])
async def start(msg: types.Message):
    await msg.answer(text.private.start)
