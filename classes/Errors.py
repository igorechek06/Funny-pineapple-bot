from src import text
from asyncio import exceptions as aex
from aiogram import exceptions as ex
from . import *


class CommandNotFound(Exception):
    def __init__(self) -> None:
        super().__init__(text.errors.CommandNotFound)


class UserNotAdmin(Exception):
    def __init__(self, id) -> None:
        super().__init__(text.errors.UserNotAdmin.format(id))


IGNORE = [
    ex.MessageNotModified,
    aex.TimeoutError
]

ERRORS = [
    CommandNotFound,
    UserNotAdmin
]
