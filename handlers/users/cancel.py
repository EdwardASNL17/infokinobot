from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(commands=['cancel'], state='*')
async def bot_parameters_height(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=True)
    await message.answer("Отменено!")
