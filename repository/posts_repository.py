from sqlalchemy import and_, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from logger import logger
from models.comments_models import Comment
from models.post_models import Post
from models.user_models import User

from .base_repository import BaseRepository


class PostRepository(BaseRepository):
    model = Post

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

    @classmethod
    async def find_one_or_none_and_comments(
        cls, session: AsyncSession, **filter_by
    ):
        try:
            query = (
                select(cls.model, User.username)
                .options(
                    joinedload(cls.model.user).load_only(User.username),
                    selectinload(cls.model.comments)
                    .joinedload(Comment.user)
                    .load_only(User.username),
                )
                .filter_by(**filter_by)
                .join(User, User.id == cls.model.user_id)
            )

            res = await session.execute(query)
            return res.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                "Ошибка при поиске записи в бд", extra={"данные": filter_by}
            )
            return None

    @classmethod
    async def find_all(
        cls, session: AsyncSession, category: str | None = None, **filter_by
    ):
        try:
            query = (
                select(cls.model.__table__.columns, User.username)
                .filter_by(**filter_by)
                .join(User, cls.model.user_id == User.id)
            )
            if not category:
                pass
            else:
                query = query.where(
                    cls.model.__table__.columns.category == category
                )
            result = await session.execute(query)
            return result.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                "Ошибка при поиске записей в бд", extra={"данные": filter_by}
            )
            return None

    @classmethod
    async def search_post(cls, text: str, session: AsyncSession):
        try:
            query = (
                select(cls.model.__table__.columns, User.username)
                .where(cls.model.title.icontains(text))
                .join(User, cls.model.user_id == User.id)
            )
            res = await session.execute(query)
            return res.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                "Ошибка при поиске записей в бд", extra={"данные": text}
            )
            return None

    @classmethod
    async def update_post(
        cls, user_id: int, post_id: int, session: AsyncSession, **data
    ):
        try:
            query = (
                update(cls.model)
                .where(
                    and_(cls.model.id == post_id, cls.model.user_id == user_id)
                )
                .values(**data)
                .returning(cls.model)
            )
            await session.execute(query)
            await session.commit()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                "Ошибка при поиске записей в бд",
                extra={
                    "данные": {
                        "user_id": user_id,
                        "post_id": post_id,
                        "data": data,
                    }
                },
            )
            return None

    @classmethod
    async def like_post(cls, post_id: int, session: AsyncSession, **data):
        try:
            query = (
                update(cls.model)
                .where(cls.model.id == post_id)
                .values(**data)
                .returning(cls.model)
            )
            await session.execute(query)
            await session.commit()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                "Ошибка при добавлении лайка на запись",
                extra={"данные": {"post_id": post_id, "data": data}},
            )
            return None
