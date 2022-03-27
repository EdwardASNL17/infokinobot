from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.users import favorites
from keyboards.inline.callback_data import favorite_movie_callback, delete_favourite_movie_callback, \
    timetable_movie_callback


def favorites_keyboard(favourite_movies):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for favourite_movie in favourite_movies:
        keyboard.insert(
            InlineKeyboardButton(text=favourite_movie[4],
                                 callback_data=favorite_movie_callback.new(movie_id=favourite_movie[3])),
        )
    return keyboard


def favourite_movie_keyboard(movie):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Купить билет🎫", url=f"{str(movie.url)}")
    ),
    keyboard.add(
        InlineKeyboardButton(text="Расписание сеансов 🎞️",
                             callback_data=timetable_movie_callback.new(movie_id=movie.id))),
    keyboard.add(InlineKeyboardButton(text="Удалить фильм из избранных 🗑",
                                      callback_data=delete_favourite_movie_callback.new(movie_id=movie.id)))
    return keyboard
