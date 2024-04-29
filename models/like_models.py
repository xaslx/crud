
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class Like(Base):
    __tablename__ = "likes"

    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True
    )

    __table_args__ = (
        Index("idx_likes_post_id", post_id),
        Index("idx_likes_user_id", user_id),
    )
