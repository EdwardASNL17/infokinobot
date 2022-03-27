from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.exceptions import BotBlocked
from gino import Gino
from sqlalchemy import String, Index, Sequence, sql, DateTime, func
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from data.config import DATABASE_URL
from .types import ChoiceType

Base = declarative_base()

database = Gino()


class BaseModel(database.Model):
    query: sql.Select

    @classmethod
    async def filter(cls, id: int):
        return await cls.query.where(cls.id == id).gino.all()

    @classmethod
    async def all(cls):
        return await cls.query.gino.all()

    @classmethod
    async def get(cls, id: int):
        return await cls.query.where(cls.id == id).gino.first()

    @classmethod
    async def get_or_create(cls, **kwargs):
        obj = None
        if 'id' in kwargs:
            obj = await cls.get(kwargs.get('id'))
        if not obj:
            obj = await cls.create(**kwargs)
        return obj

    @classmethod
    async def count(cls) -> int:
        return await database.func.count(cls.id).gino.scalar()


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True)
    first_name = Column(String(128))
    username = Column(String(128))
    city = Column(String(128))
    _idx = Index('user_id_index', 'id')

    @staticmethod
    async def mailing(bot: Bot, text: str, keyboard: InlineKeyboardMarkup = None) -> int:
        count_users = 0
        for user in await User.query.gino.all():
            try:
                await bot.send_message(chat_id=user.id, text=text, reply_markup=keyboard)
                count_users += 1
            except BotBlocked:
                pass
        return count_users


class UserFavorite(BaseModel):
    __tablename__ = 'user_favorites'

    id = Column(Integer, Sequence('user_favorites_id_seq'), primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))

    _idx = Index('user_favorites_id_index', 'id')


class Movie(BaseModel):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    year = Column(String)
    header = Column(String)
    synopsis = Column(String)
    country = Column(String)
    director = Column(String)
    duration = Column(String)
    age_rating = Column(String)
    url = Column(String)

    _idx = Index('movies_id_index', 'id')


class MovieReview(BaseModel):
    __tablename__ = 'movies_reviews'

    id = Column(Integer, Sequence('movies_reviews_id_seq'), primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    text = Column(String)
    _idx = Index('movies_reviews_id_index', 'id')


class UserNotification(BaseModel):
    __tablename__ = 'users_notification'

    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    _idx = Index('users_notification_id_index', 'id')


async def create_database():
    await database.set_bind(DATABASE_URL)
    try:
        await database.gino.create_all()
    except InvalidRequestError:
        pass
