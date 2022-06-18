from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink
from sqlalchemy import and_, func

from keyboards.default.menu import MOVIE
from keyboards.inline.afisha import afisha_movie_keyboard
from keyboards.inline.getmovie import search_result_movies_keyboard
from loader import dp
from states.getmovie import UserGetMovieState
from utils.db_api.database import UserFavorite, Movie


@dp.message_handler(commands=['search'], state='*')
@dp.message_handler(text=MOVIE, state='*')
async def get_movie(message: types.Message):
    await message.answer(f"Введи название фильма, который ты хочешь найти")
    await UserGetMovieState.get.set()


@dp.message_handler(content_types=['text'], state=UserGetMovieState.get)
async def give_movie(message: types.Message, state: FSMContext):
    await state.update_data(movie=message.text)
    await state.reset_state(with_data=True)
    movies = await Movie.query.where(func.lower(Movie.name).like(func.lower(f'%{message.text}%'))).gino.all()
    if movies:
        await message.answer(
            f"🔍 Поиск по \"{message.text}\":", reply_markup=search_result_movies_keyboard(movies=movies)
        )
    else:
        await message.answer(f"Фильма {message.text} нет в базе данных")
