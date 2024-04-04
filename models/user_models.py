from datetime import date, datetime

from sqlalchemy import Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base

from .post_models import Post


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    registered_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow()
    )
    role: Mapped[str] = mapped_column(default="user")
    email: Mapped[str]
    date_of_birthday: Mapped[date] = mapped_column(Date)
    is_banned: Mapped[bool] = mapped_column(default=False, nullable=False)
    hashed_password: Mapped[str]
    image_url: Mapped[str] = mapped_column(
        default="/static/user_photo/default"
    )

    posts: Mapped[list["Post"]] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.username}"
