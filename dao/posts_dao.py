from sqlalchemy import and_, join, select, update

from database.database import async_session_maker
from models.post_models import Post
from models.user_models import User

from .base import BaseDAO


class PostDAO(BaseDAO):
    model = Post

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__.columns, User.username)
                .filter_by(**filter_by)
                .join(User, cls.model.user_id == User.id)
            )
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__.columns)
                .filter_by(**filter_by)
                .order_by(
                    cls.model.__table__.columns.date_of_publication.desc()
                )
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_all_join(cls, category: str | None = None, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__.columns, User.username)
                .filter_by(**filter_by)
                .join(User, cls.model.user_id == User.id)
                .order_by(
                    cls.model.__table__.columns.date_of_publication.desc()
                )
            )
            if not category:
                pass
            else:
                query = query.where(
                    cls.model.__table__.columns.category == category
                )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def update_post(cls, user_id: int, post_id: int, **data):
        query = (
            update(cls.model)
            .where(and_(cls.model.id == post_id, cls.model.user_id == user_id))
            .values(**data)
        )
        async with async_session_maker() as session:
            await session.execute(query)
            await session.commit()
