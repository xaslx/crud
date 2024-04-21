from datetime import datetime
from enum import Enum
from .users_schemas import UserAfterRegister
from pydantic import BaseModel, ConfigDict, Field


class Category(str, Enum):
    films = "Фильмы"
    series = "Сериалы"
    games = "Игры"
    sport = "Спорт"
    other = "Другое"
    programming = "Программирование"


class Posts(BaseModel):
    id: int
    title: str
    user_id: int
    content: str
    date_of_publication: datetime
    date_of_update: datetime
    likes: int
    category: str
    username: str

    model_config = ConfigDict(from_attributes=True)


class MyPosts(BaseModel):
    id: int
    title: str
    user_id: int
    content: str
    date_of_publication: datetime
    date_of_update: datetime
    likes: int
    category: str

    model_config = ConfigDict(from_attributes=True)


class PostsUser(Posts):
    username: str
    model_config = ConfigDict(from_attributes=True)


class PostsIn(BaseModel):
    title: str = Field(min_length=5, max_length=25)
    content: str = Field(min_length=10, max_length=2500)
    model_config = ConfigDict(from_attributes=True)
