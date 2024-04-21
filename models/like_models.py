from database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .post_models import Post
    from .user_models import User


class Like(Base):
    __tablename__ = 'likes'

    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
