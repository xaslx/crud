from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, String, desc
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base

from .comments_models import Comment

if TYPE_CHECKING:
    from .user_models import User


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(25))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(String(2000))
    date_of_publication: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow()
    )
    date_of_update: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow()
    )
    likes: Mapped[int] = mapped_column(default=0)

    category: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="post", order_by=lambda: desc(Comment.created_at)
    )

    __table_args__ = (
        Index("idx_post_title", title),
        Index("idx_post_user_id", user_id),
        Index("idx_post_date_of_publication", date_of_publication),
    )

    def __str__(self):
        return f"{self.title}"
