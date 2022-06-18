from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import get_afisha_movie_callback


def search_result_movies_keyboard(movies):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for movie in movies:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{movie.name} ({movie.year})", callback_data=get_afisha_movie_callback.new(movie_id=movie.id)
            )
        )
    return keyboard
