from typing import List

from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink
from sqlalchemy import and_

import data
from keyboards.default.menu import FAVORITES
from keyboards.inline.callback_data import favorite_movie_callback, delete_favourite_movie_callback
from keyboards.inline.favorites import favorites_keyboard, favourite_movie_keyboard
from loader import dp
from utils.db_api.database import User, UserFavorite, Movie


@dp.message_handler(commands=['favorites'], state='*')
@dp.message_handler(text=FAVORITES, state='*')
async def bot_favorites(message: types.Message):
    favorites: List[UserFavorite] = await UserFavorite.join(Movie).select().where(
        UserFavorite.user_id == message.from_user.id).gino.all()
    text = ""
    for favorite in favorites:
        text += f"{favorite[4]}\n"
    if len(text) > 0:
        await message.answer(f"<b>Ваши избранные фильмы</b>\n\n{text}", reply_markup=favorites_keyboard(favorites))
    else:
        await message.answer(f"Список избранных пуст")


@dp.callback_query_handler(favorite_movie_callback.filter(), state='*')
async def bot_favorite_callback(call: CallbackQuery, callback_data: dict):
    movie = await Movie.query.where(Movie.id == int(callback_data["movie_id"])).gino.first()
    movie_text = f"{movie.name} ({movie.year})"
    await call.message.edit_text(
        "\n".join(
            [
                f"<b>{hlink(movie_text, movie.url)}</b>\nРежиссер: {movie.director}\n",
                f"<b>{movie.header}</b>\n{movie.synopsis}\n{movie.age_rating}",
            ]
        ), reply_markup=favourite_movie_keyboard(movie)
    )


@dp.callback_query_handler(delete_favourite_movie_callback.filter(), state='*')
async def delete_favourite_movie_callback(call: CallbackQuery, callback_data: dict):
    favorite = await UserFavorite.query.where(and_(UserFavorite.movie_id == int(callback_data["movie_id"]),
                                                   UserFavorite.user_id == call.from_user.id)).gino.first()
    await favorite.delete()
    await call.answer("Фильм был успешно удален из избранных")
