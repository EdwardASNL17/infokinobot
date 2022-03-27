from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import menu
from loader import dp
from states.start import UserStartState
from utils.db_api.database import User


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! Введи свой город, чтобы я мог предложить тебе верные данные об афише",
        reply_markup=menu)
    await UserStartState.city.set()


@dp.message_handler(content_types=['text'], state=UserStartState.city)
async def bot_set_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()
    await state.reset_state(with_data=True)
    user = await User.get_or_create(
        id=message.from_user.id, first_name=message.from_user.first_name, username=message.from_user.username,
        city=data['city']
    )
    if user:
        await user.update(city=data['city']).apply()
        await message.answer(f"Данные успешно изменены")
    else:
        await message.answer(f"Данные успешно сохранены")
