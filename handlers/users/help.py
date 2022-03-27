from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state='*')
async def bot_help(message: types.Message):
    text = (
        "Список команд: ",
        "/start - Начать диалог с ботом для прохождения регистрации",
        "/help - Получить справку о работе команд",
        "/city - Получить информацию о своем городе",
        "/afisha - Получить информацию об афише кинопроката на сегодня",
        "/favorites - Получить список избранных фильмов",
        "/search - Поиск фильма по названию"
    )

    await message.answer("\n".join(text))
