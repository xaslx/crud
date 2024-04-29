from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from logger import logger
from models.like_models import Like
from models.post_models import Post

from .base_repository import BaseRepository


class LikeRepository(BaseRepository):
    model = Like

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        try:
            query = (
                select(
                    cls.model.__table__.columns, Post.title.label("post_title")
                )
                .filter_by(**filter_by)
                .join(Post, Post.id == cls.model.post_id)
            )
            result = await session.execute(query)
            return result.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                "Ошибка при поиске значений", extra={"данные": filter_by}
            )
            return None
