from aiogram.dispatcher.filters.state import StatesGroup, State


class UserGetMovieState(StatesGroup):
    get = State()
    give = State()