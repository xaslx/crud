from datetime import datetime

from sqlalchemy import DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base

from .comments_models import Comment
from .post_models import Post


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(15), unique=True)
    registered_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow()
    )
    role: Mapped[str] = mapped_column(default="user")
    email: Mapped[str] = mapped_column(String(30), unique=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_banned: Mapped[bool] = mapped_column(default=False, nullable=False)
    hashed_password: Mapped[str]
    image_url: Mapped[str] = mapped_column(default="default.webp")

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")

    __table_args__ = (
        Index("idx_username", username),
        Index("idx_email", email),
    )

    def __str__(self):
        return f"{self.username}"
