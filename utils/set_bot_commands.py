from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("city", "Изменить город"),
            types.BotCommand("afisha", "Получить афишу"),
            types.BotCommand("search", "Поиск фильма"),
            types.BotCommand("favorites", "Избранные фильмы"),
        ]
    )
