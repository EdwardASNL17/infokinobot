from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import add_favorites_callback


def movie_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Добавить фильм в избранные", callback_data=add_favorites_callback.new())
    ),
    return keyboard
