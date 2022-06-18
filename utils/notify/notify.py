import asyncio
from datetime import datetime

from aiogram.utils.markdown import hlink

from data.config import TIME_BETWEEN_NOTIFICATION_UPDATES
from keyboards.inline.afisha import afisha_keyboard
from loader import dp, tz
from utils.afisha.notify_parser import notify_parser
from utils.db_api.database import User, UserNotification


async def notify_users(time_between_notification_updates: int = TIME_BETWEEN_NOTIFICATION_UPDATES):
    while True:
        today = datetime.now(tz=tz).date()
        today.weekday()
        if today.weekday() == 2:
            movies = await notify_parser()

            text = f"Сегодня в прокат вышли следующие фильмы:\n\n"
            for movie in movies:
                text += f"{hlink(movie['name'], movie['link'])}\n"
            for user in await UserNotification.all():
                try:
                    await dp.bot.send_message(chat_id=user.user_id, text=text, reply_markup=afisha_keyboard(movies))
                except:
                    pass
        await asyncio.sleep(time_between_notification_updates)
