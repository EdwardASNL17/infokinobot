from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.default.menu import AFISHA
from keyboards.inline.callback_data import get_release_calendar_callback, check_pushkard_afisha_callback, \
    get_afisha_movie_callback, add_favorite_movie_callback, timetable_movie_callback, \
    delete_favourite_movie_callback, change_notification_callback, check_reviews_callback, get_afisha_callback


def afisha_keyboard(afisha_movies):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for afisha_movie in afisha_movies:
        keyboard.insert(
            InlineKeyboardButton(text=afisha_movie['name'],
                                 callback_data=get_afisha_movie_callback.new(movie_id=afisha_movie['id'])),
        )
    keyboard.add(
        InlineKeyboardButton(text="Скоро в кино 📅", callback_data=get_release_calendar_callback.new())
    ),
    keyboard.add(
        InlineKeyboardButton(text="Пушкинская Карта 💳", callback_data=check_pushkard_afisha_callback.new())
    ),
    return keyboard


def coming_soon_keyboard(soon_movies, notification):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for soon_movie in soon_movies:
        keyboard.insert(
            InlineKeyboardButton(text=soon_movie['name'],
                                 callback_data=get_afisha_movie_callback.new(movie_id=soon_movie['id'])),
        )
    if notification:
        keyboard.add(
            InlineKeyboardButton(text="Отключить уведомления 🔕", callback_data=change_notification_callback.new()))
    else:
        keyboard.add(
            InlineKeyboardButton(text="Включить уведомления 🔔", callback_data=change_notification_callback.new()))
    return keyboard


def afisha_movie_keyboard(movie, favorite, back_to_afisha=False):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Расписание сеансов 🎞️",
                             callback_data=timetable_movie_callback.new(movie_id=movie.id))
    ),
    keyboard.add(
        InlineKeyboardButton(text="Купить билет 🎫", url=f"{str(movie.url)}")
    ),
    if favorite:
        keyboard.add(
            InlineKeyboardButton(text="Удалить фильм из избранных 🗑️",
                                 callback_data=delete_favourite_movie_callback.new(movie_id=movie.id))
        ),
    else:
        keyboard.add(
            InlineKeyboardButton(text="Добавить фильм в избранные 💞",
                                 callback_data=add_favorite_movie_callback.new(movie_id=movie.id))
        )
    keyboard.add(
        InlineKeyboardButton(text="Просмотреть отзывы 📃", callback_data=check_reviews_callback.new(movie_id=movie.id))
    )
    keyboard.add(
        InlineKeyboardButton(text=AFISHA, callback_data=get_afisha_callback.new())
    )
    return keyboard


def pushkard_keyboard(movies):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for movie in movies:
        keyboard.insert(
            InlineKeyboardButton(text=movie['name'],
                                 callback_data=get_afisha_movie_callback.new(movie_id=movie['id'])),
        )
    keyboard.add(
        InlineKeyboardButton(text="Оформить Пушкинскую Карту💳", url="https://www.culture.ru/pushkinskaya-karta")
    ),
    return keyboard


def timetable_keyboard(movie_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="🔙", callback_data=get_afisha_movie_callback.new(movie_id=movie_id))
    )
    return keyboard
