from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from schemas.comments_schemas import CommentOut

from .users_schemas import UserShort


class Category(Enum):
    films = "Фильмы"
    series = "Сериалы"
    games = "Игры"
    sport = "Спорт"
    other = "Другое"
    programming = "Программирование"


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


class Posts(MyPosts):
    username: str

    model_config = ConfigDict(from_attributes=True)


class PostsIn(BaseModel):
    title: str = Field(max_length=25, min_length=5)
    content: str = Field(max_length=2000, min_length=10)
    category: Category


class PostWComments(MyPosts):
    user: UserShort
    comments: list[CommentOut]
