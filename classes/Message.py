import re
from typing import *

from aiogram import types
from bot import bot

from .Errors import *


class Data:
    def __init__(self, data: dict, id: int) -> None:
        self.storage: dict = data
        self.id = id

    def __enter__(self):
        return self.storage

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __getitem__(self, key):
        return self.storage[key]

    def __setitem__(self, key, value):
        self.storage[key] = value

    def __iter__(self):
        for key in self.storage:
            yield key

    def __str__(self):
        return str(self.storage)

    def __repr__(self) -> dict:
        return self.storage


class MessageData:

    def __init__(self) -> None:
        self.storage: Dict[int, Data] = {}
        self._msgs: List[types.Message] = []

    def __call__(self, message: types.Message) -> Data:
        key = message.message_id
        if key not in self.storage:
            self._msgs.append(message)
            self.storage[key] = Data({}, key)

        return self.storage[key]

    async def remove_data(self, message_id: types.Message):
        self.storage.pop(message_id)
        for num, msg in enumerate(self._msgs):
            if message_id == msg.message_id:
                self._msgs.pop(num)
                break

    async def del_all(self):
        for msg in self._msgs:
            await msg.delete()
            self.storage.pop(msg.message_id)
