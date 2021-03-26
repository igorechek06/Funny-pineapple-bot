from typing import List
from aiogram import types
from bot import bot, dp
from config import bot_id, pineapple_chat
from classes.Errors import UserNotAdmin

from src import buttons, text
from objects import MessageData

pull: List[types.User] = []


def chat(msg: types.Message):
    return msg.chat.type in ["group", "supergroup"]


def in_pull(msg: types.Message):
    user = msg.left_chat_member
    for u in pull:
        if u.id == user.id:
            return True
    return False


def bot_add(msg: types.Message):
    for user in msg.new_chat_members:
        if user.id == bot_id:
            return True

    return False


@dp.message_handler(lambda msg: chat(msg) and bot_add(msg), content_types=types.ContentType.NEW_CHAT_MEMBERS)
# @dp.message_handler(lambda msg: chat(msg), commands=["start"])
async def start(msg: types.Message):
    if msg.chat.id == pineapple_chat:
        await msg.answer(text.chat.start_pineapple)
    else:
        await msg.answer(text.chat.start_not_pineapple)
        await bot.leave_chat(msg.chat.id)


@dp.message_handler(lambda msg: chat(msg), content_types=types.ContentType.NEW_CHAT_MEMBERS)
# @dp.message_handler(lambda msg: chat(msg), commands=["new"])
async def new_member(msg: types.Message):
    await msg.delete()
    await msg.chat.restrict(msg.from_user.id,
                            can_send_messages=False,
                            can_send_media_messages=False,
                            can_send_other_messages=False,
                            can_add_web_page_previews=False)
    message = await msg.answer(text.chat.new_member, reply_markup=buttons.chat.new_member)
    pull.append(msg.from_user)
    with MessageData(message) as data:
        data["user"] = msg.from_user


@dp.message_handler(lambda msg: chat(msg) and in_pull(msg), content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def leave_member(msg: types.Message):
    await msg.delete()
    for data in MessageData.storage.values():
        user: types.User = data["user"]
        if user.id == msg.left_chat_member.id:
            pull.remove(user)
            await msg.chat.delete_message(data.id)
            await MessageData.remove_data(data.id)


@dp.callback_query_handler(lambda msg: msg.data in ["accept", "decline"])
async def new_member_buttons(callback: types.CallbackQuery):
    member = await callback.message.chat.get_member(callback.from_user.id)
    if not member.is_chat_admin():
        raise UserNotAdmin(member.user.id)

    with MessageData(callback.message) as data:
        user: types.User = data["user"]

    if callback.data == "accept":
        await callback.message.chat.restrict(user.id,
                                             can_send_messages=True,
                                             can_send_media_messages=True,
                                             can_send_other_messages=True,
                                             can_add_web_page_previews=True
                                             )
    else:
        await callback.message.chat.kick(user.id)

    await callback.message.delete()

# @dp.message_handler(commands=["leave"])
# async def leave(msg: types.Message):
#     await bot.leave_chat(msg.chat.id)
