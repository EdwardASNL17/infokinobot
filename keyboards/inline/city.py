from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import change_city_callback


def city_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Изменить город 🏙️", callback_data=change_city_callback.new())
    ),
    return keyboard
