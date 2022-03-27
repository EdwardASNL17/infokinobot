from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

CITY = "🏙️ Город"
AFISHA = "📰 Афиша"
FAVORITES = "🎬 Избранные"
MOVIE = "🔍 Поиск фильма"

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(CITY)
        ],
        [
            KeyboardButton(AFISHA)
        ],
        [
            KeyboardButton(FAVORITES)
        ],
        [
            KeyboardButton(MOVIE)
        ]
    ],
    resize_keyboard=True
)
