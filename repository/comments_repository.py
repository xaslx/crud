from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from logger import logger
from models.comments_models import Comment
from models.user_models import User

from .base_repository import BaseRepository


class CommentRepository(BaseRepository):
    model = Comment

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        try:
            query = (
                select(cls.model.__table__.columns, User.username)
                .filter_by(**filter_by)
                .join(User, cls.model.user_id == User.id)
            )
            result = await session.execute(query)
            return result.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                "Ошибка при поиске записи в бд", extra={"данные": filter_by}
            )
            return None
