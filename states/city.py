from aiogram.dispatcher.filters.state import StatesGroup, State


class UserCityState(StatesGroup):
    change = State()
