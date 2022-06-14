from datetime import date
from typing import List

from aiogram.utils.markdown import hlink
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import and_

from keyboards.default.menu import CITY, AFISHA
from keyboards.inline.afisha import afisha_keyboard, pushkard_keyboard, afisha_movie_keyboard, coming_soon_keyboard
from keyboards.inline.callback_data import get_release_calendar_callback, check_pushkard_afisha_callback, \
    get_afisha_movie_callback, add_favorite_movie_callback, timetable_movie_callback, \
    change_notification_callback
from loader import dp
from utils.afisha.afisha_parser import parsing_afisha
from utils.afisha.release_calendar_parser import parsing_releases
from utils.db_api.database import User, UserFavorite, Movie, UserNotification
from bs4 import BeautifulSoup
import requests

today = date.today()


@dp.message_handler(commands=['afisha'], state='*')
@dp.message_handler(text=AFISHA, state='*')
async def get_afisha(message: types.Message):
    user = await User.query.where(User.id == message.from_user.id).gino.first()

    cities = {"Москва": "msk", "Санкт-Петербург": "spb", "Таганрог": "taganrog", "Казань": "kazan",
              "Калининград": "kaliningrad", "Ростов-на-Дону": "rostov-na-donu"}

    url = f"https://www.afisha.ru/{cities[user.city]}/schedule_cinema/na-segodnya/"
    movies = await parsing_afisha(url)
    text = f"Афиша на {today.strftime('%d.%m.%y')}🎥\n\n"
    for movie in movies:
        text += f"{hlink(movie['name'], movie['link'])}\n"

    await message.answer(text, reply_markup=afisha_keyboard(movies))
    for movie in movies:
        await Movie.get_or_create(id=movie['id'], name=movie['name'], year=movie["year"], header=movie["header"],
                                  synopsis=movie['synopsis'], country=movie['country'], director=movie['director'],
                                  duration=movie['duration'], age_rating=movie['age_rating'], url=movie['link'])


@dp.callback_query_handler(get_afisha_movie_callback.filter(), state='*')
async def bot_afisha_movie_callback(call: CallbackQuery, callback_data: dict):
    movie = await Movie.query.where(Movie.id == int(callback_data["movie_id"])).gino.first()
    favorite = await UserFavorite.query.where(and_(UserFavorite.movie_id == int(callback_data["movie_id"]),
                                                   UserFavorite.user_id == call.from_user.id)).gino.first()
    movie_text = f"{movie.name} ({movie.year})"
    await call.message.answer(
        "\n".join(
            [
                f"<b>{hlink(movie_text, movie.url)}</b>\nРежиссер: {movie.director}\n",
                f"<b>{movie.header}</b>\n{movie.synopsis}\n{movie.age_rating}",
            ]
        ), reply_markup=afisha_movie_keyboard(movie, favorite)
    )


@dp.callback_query_handler(add_favorite_movie_callback.filter(), state='*')
async def add_favourite_movie_callback(call: CallbackQuery, callback_data: dict):
    movie = await Movie.query.where(Movie.id == int(callback_data["movie_id"])).gino.first()
    await UserFavorite.get_or_create(user_id=call.from_user.id, movie_id=movie.id)
    await call.message.answer(f"Фильм {movie.name} был успешно добавлен в избранное")


@dp.callback_query_handler(get_release_calendar_callback.filter(), state='*')
async def bot_release_calendar_callback(call: CallbackQuery, callback_data: dict):
    notification = await UserNotification.query.where(UserNotification.user_id == call.from_user.id).gino.first()
    url = "https://www.afisha.ru/data-vyhoda/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    release_date = soup.find('div', class_='_3Yfoo').text
    movies = await parsing_releases(url)
    text = f"Cкоро в кино 📅\n\n<b>{release_date}</b>\n"
    for movie in movies:
        text += f"{hlink(movie['name'], movie['link'])}\n"
    await call.message.answer(text, reply_markup=coming_soon_keyboard(movies, notification))

    for movie in movies:
        await Movie.get_or_create(id=movie['id'], name=movie['name'], year=movie["year"], synopsis=movie['synopsis'],
                                  url=movie['link'])


@dp.callback_query_handler(change_notification_callback.filter(), state='*')
async def bot_change_notification_callback(call: CallbackQuery, callback_data: dict):
    notification = await UserNotification.query.where(UserNotification.user_id == call.from_user.id).gino.first()
    if notification:
        await notification.delete()
        await call.answer("Уведомления выключены 🔕")
    else:
        await UserNotification.get_or_create(user_id=call.from_user.id)
        await call.answer("Уведомления включены 🔔")


@dp.callback_query_handler(check_pushkard_afisha_callback.filter(), state='*')
async def bot_pushkard_callback(call: CallbackQuery, callback_data: dict):
    user = await User.query.where(User.id == call.from_user.id).gino.first()
    cities = {"Москва": "msk", "Санкт-Петербург": "spb", "Таганрог": "taganrog", "Казань": "kazan",
              "Калининград": "kaliningrad", "Ростов-на-Дону": "rostov-na-donu"}
    url = f"https://www.afisha.ru/{cities[user.city]}/schedule_cinema/na-segodnya/pushkincard/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    movies = soup.findAll('div', class_='_1kwbj lkWIA _2Ds3f')
    text = f"Пушкинская Карта 💳\n\n"
    for movie in movies:
        movie['link'] = "https://www.afisha.ru" + movie.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').get('href')
        movie['id'] = int(movie['link'].split("/")[4])
        movie['name'] = movie.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').find('h2', class_='_3Yfoo').text
        movie['year'] = movie.find('div', class_='_2jztV _2Nzs2 _2XtXq').find('span', class_='_1gC4P').text
        text += f"{hlink(movie['name'], movie['link'])}\n"
        req = requests.get(movie['link'])
        soup = BeautifulSoup(req.text, 'lxml')
        if soup.find('h2', class_='_3Yfoo'):
            movie['header'] = soup.find('h2', class_='_3Yfoo').text
        else:
            movie['header'] = ""
        if soup.find('div', class_='_1kwbj lkWIA _2Ds3f').find('p'):
            movie['synopsis'] = soup.find('div', class_='_1kwbj lkWIA _2Ds3f').find('p').text
        else:
            movie['synopsis'] = ""
        infoCount = soup.find_all('span', class_='h1Lfd')
        info = soup.find_all('span', class_='_1gC4P')
        movie['country'] = info[0].text
        check = infoCount[2].text
        if check == "Режиссер" or check == "Режиссеры":
            movie['director'] = info[2].text
            if infoCount[3].text == "Продолжительность":
                movie['duration'] = info[3].text
            else:
                movie['duration'] = ''
        else:
            movie['director'] = ''
            movie['duration'] = info[2].text
        movie['age_rating'] = info[len(infoCount) - 2].text

    if movies:
        print("work")
    else:
        text += "На сегодняшний день нет фильмов, доступных по Пушкинской карте"

    await call.message.answer(text, reply_markup=pushkard_keyboard(movies))
    for movie in movies:
        await Movie.get_or_create(id=movie['id'], name=movie['name'], year=movie["year"],
                                  synopsis=movie['synopsis'], url=movie['link'])


@dp.callback_query_handler(timetable_movie_callback.filter(), state='*')
async def bot_timetable_callback(call: CallbackQuery, callback_data: dict):
    user = await User.query.where(User.id == call.from_user.id).gino.first()
    movie = await Movie.query.where(Movie.id == int(callback_data['movie_id'])).gino.first()
    cities = {"Москва": "msk", "Санкт-Петербург": "spb", "Таганрог": "taganrog", "Казань": "kazan",
              "Калининград": "kaliningrad", "Ростов-на-Дону": "rostov-na-donu"}
    url = f"https://www.afisha.ru/{cities[user.city]}/schedule_cinema_product/{movie.id}/"
    r = requests.get(url)
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
        await call.message.answer(text)
    else:
        await call.message.answer("В данный момент сеансов на фильм нет")
