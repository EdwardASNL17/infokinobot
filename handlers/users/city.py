from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.users.afisha import cities
from keyboards.default.menu import CITY
from keyboards.inline.callback_data import change_city_callback
from keyboards.inline.city import city_keyboard
from loader import dp
from states.city import UserCityState
from utils.db_api.database import User


@dp.message_handler(commands=['city'], state='*')
@dp.message_handler(text=CITY, state='*')
async def bot_city(message: types.Message):
    user = await User.query.where(User.id == message.from_user.id).gino.first()
    if user:
        await message.answer(
            "\n".join(
                [
                    f"Ваш город: {user.city}"
                ]
            ),
            reply_markup=city_keyboard()
        )
    else:
        await message.answer("Вы не зарегистрированы в системе")


@dp.callback_query_handler(change_city_callback.filter(), state='*')
async def bot_change_city_callback(call: CallbackQuery, callback_data: dict):
    await call.message.answer(f"Введи город, для которого ты хочешь получать самую свежую афишу")
    await UserCityState.change.set()


@dp.message_handler(content_types=['text'], state=UserCityState.change)
async def bot_city_change(message: types.Message, state: FSMContext):
    if message.text in cities:
        user = await User.query.where(User.id == message.from_user.id).gino.first()
        await state.reset_state(with_data=True)
        await user.update(city=message.text).apply()
        await message.answer(f"Данные успешно изменены.\nТвой город: {user.city}")
    else:
        await message.answer(f"Попробуйте другой город")