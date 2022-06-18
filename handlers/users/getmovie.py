from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink
from sqlalchemy import and_, func

from keyboards.default.menu import MOVIE
from keyboards.inline.afisha import afisha_movie_keyboard
from keyboards.inline.callback_data import add_favorites_callback
from keyboards.inline.getmovie import movie_keyboard
from states.getmovie import UserGetMovieState
from loader import dp
from utils.db_api.database import User, UserFavorite, Movie


@dp.message_handler(commands=['search'], state='*')
@dp.message_handler(text=MOVIE, state='*')
async def get_movie(message: types.Message):
    await message.answer(f"Введи название фильма, который ты хочешь найти")
    await UserGetMovieState.get.set()


@dp.message_handler(content_types=['text'], state=UserGetMovieState.get)
async def give_movie(message: types.Message, state: FSMContext):
    await state.update_data(movie=message.text)
    await state.reset_state(with_data=True)
    movies = await Movie.query.where(Movie.name.like(func.lower(f'%{message.text}%')).lower()).gino.all()
    if movies:
        for movie in movies:
            favorite = await UserFavorite.query.where(and_(UserFavorite.movie_id == int(movie.id),
                                                           UserFavorite.user_id == message.from_user.id)).gino.first()
            await message.answer(
                "\n".join(
                    [
                        f"<b>{hlink(f'{movie.name} ({movie.year})', movie.url)}</b>\n",
                        f"{movie.synopsis}"
                    ]
                ), reply_markup=afisha_movie_keyboard(movie, favorite)
            )
    else:
        await message.answer(f"Фильма {message.text} нет в базе данных")
