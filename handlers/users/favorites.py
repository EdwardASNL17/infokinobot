from typing import List

import requests
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink
from bs4 import BeautifulSoup
from sqlalchemy import and_

import data
from handlers.users.afisha import bot_afisha_movie_callback, cities
from keyboards.default.menu import FAVORITES
from keyboards.inline.afisha import afisha_movie_keyboard, timetable_keyboard
from keyboards.inline.callback_data import favorite_movie_callback, delete_favourite_movie_callback, \
    get_favorites_callback, timetable_movie_callback, timetable_favorite_callback, delete_from_favorite_movie_callback, \
    add_from_favorite_movie_callback
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


@dp.callback_query_handler(get_favorites_callback.filter(), state='*')
async def get_favorites_callback(call: CallbackQuery, callback_data: dict):
    favorites: List[UserFavorite] = await UserFavorite.join(Movie).select().where(
        UserFavorite.user_id == call.from_user.id).gino.all()
    text = ""
    for favorite in favorites:
        text += f"{favorite[4]}\n"
    if len(text) > 0:
        await call.message.edit_text(f"<b>Ваши избранные фильмы</b>\n\n{text}",
                                     reply_markup=favorites_keyboard(favorites))
    else:
        await call.message.edit_text(f"Список избранных пуст")


@dp.callback_query_handler(favorite_movie_callback.filter(), state='*')
async def bot_favorite_callback(call: CallbackQuery, callback_data: dict):
    movie = await Movie.query.where(Movie.id == int(callback_data["movie_id"])).gino.first()
    favorite = await UserFavorite.query.where(and_(UserFavorite.movie_id == int(callback_data["movie_id"]),
                                                   UserFavorite.user_id == call.from_user.id)).gino.first()
    movie_text = f"{movie.name} ({movie.year})"
    await call.message.edit_text(
        "\n".join(
            [
                f"<b>{hlink(movie_text, movie.url)}</b>\nРежиссер: {movie.director}\n",
                f"<b>{movie.header}</b>\n{movie.synopsis}\n{movie.age_rating}",
            ]
        ), reply_markup=afisha_movie_keyboard(movie, favorite, back_to_favorites=True)
    )


@dp.callback_query_handler(delete_from_favorite_movie_callback.filter(), state='*')
async def delete_from_favorite_movie_callback(call: CallbackQuery, callback_data: dict):
    favorite = await UserFavorite.query.where(and_(UserFavorite.movie_id == int(callback_data["movie_id"]),
                                                   UserFavorite.user_id == call.from_user.id)).gino.first()
    if favorite:
        await favorite.delete()
        await call.answer("Фильм был успешно удален из избранных")
        await bot_favorite_callback(call, callback_data)


@dp.callback_query_handler(add_from_favorite_movie_callback.filter(), state='*')
async def add_from_favorite_movie_callback(call: CallbackQuery, callback_data: dict):
    movie = await Movie.query.where(Movie.id == int(callback_data["movie_id"])).gino.first()
    await UserFavorite.get_or_create(user_id=call.from_user.id, movie_id=movie.id)
    await call.answer(f"Фильм {movie.name} был успешно добавлен в избранные")
    await bot_favorite_callback(call, callback_data)


@dp.callback_query_handler(timetable_favorite_callback.filter(), state='*')
async def bot_timetable_favorite_callback(call: CallbackQuery, callback_data: dict):
    user = await User.query.where(User.id == call.from_user.id).gino.first()
    movie = await Movie.query.where(Movie.id == int(callback_data['movie_id'])).gino.first()
    url = f"https://www.afisha.ru/{cities[user.city]}/schedule_cinema_product/{movie.id}/"
    r = requests.get(url)
    if len(r.history) == 0:
        soup = BeautifulSoup(r.text, 'lxml')
        if soup.find('div', class_='_3zDWC _3x7YU _2cFJG hkScZ'):
            count_pages = len(soup.find('div', class_='_3zDWC _3x7YU _2cFJG hkScZ').find_all('button')) - 2
            if count_pages > 2:
                count_pages = 2
        else:
            count_pages = 1
        text = f"<b>Расписание сеансов фильма {movie.name} в городе {user.city}\n</b>"
        if soup.find('span', class_='_8FVfk'):
            date = soup.find('span', class_='_8FVfk').text
            month = soup.find('span', class_='_1u5fN').text.lower().split("ь")[0] + "я"
            text += f"Ближайшая дата сеанса: {date} {month}\n\n"
            for i in range(1, count_pages + 1):
                url = f"https://www.afisha.ru/{cities[user.city]}/schedule_cinema_product/{movie.id}/page{i}/"
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'lxml')
                cinemas = soup.findAll('div', class_='_2Pfqq _2X8EE')
                for cinema in cinemas:
                    cinema['link'] = "https://www.afisha.ru" + cinema.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').get(
                        'href')
                    cinema['name'] = cinema.find('h2', class_='_3Yfoo').text
                    text += f"<b>{hlink(cinema['name'], cinema['link'])}</b>\nСеансы\n"
                    seances = cinema.findAll('div', class_='_1sRLP')
                    for seance in seances:
                        seance['time'] = seance.find('button', '_3jiFM _1Lyrw NYM3K _2oJKT _2IYn8 _1ORu2').text
                        if seance.findAll('div', '_1dje5 _2qUBY'):
                            if len(seance.findAll('div', '_1dje5 _2qUBY')) > 1:
                                seance['price'] = seance.findAll('div', '_1dje5 _2qUBY')[0].text + " " + \
                                                  seance.findAll('div', '_1dje5 _2qUBY')[1].text
                            else:
                                seance['price'] = seance.find('div', '_1dje5 _2qUBY').text
                            text += f"{seance['time']} {seance['price']}\n"
                        else:
                            seance['price'] = "Билеты продаются в кассе или на сайте кинотеатра"
                            text += f"{seance['time']} {seance['price']}\n"
            await call.message.edit_text(text, reply_markup=timetable_keyboard(movie_id=movie.id,
                                                                               back_to_favorite=True))
        else:
            await call.answer("В данный момент сеансов на фильм нет")
    else:
        await call.answer(f"{movie.name} не прокатывается в вашем городе")
