from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base

if TYPE_CHECKING:
    from .user_models import User


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str]
    date_of_publication: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow()
    )
    date_of_update: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow()
    )
    likes: Mapped[int] = mapped_column(default=0)
    category: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="posts")

    def __str__(self):
        return f"{self.title}"
