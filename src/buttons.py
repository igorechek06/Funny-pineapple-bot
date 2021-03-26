from aiogram.types import InlineKeyboardMarkup as IM
from aiogram.types import InlineKeyboardButton as IB


class chat:
    new_member = IM().add(
        IB("Ананас 🍍", callback_data="accept"),
        IB("Импостер 📮", callback_data="decline")
    )
