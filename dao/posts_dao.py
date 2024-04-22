from sqlalchemy import and_, join, select, update
from logger import logger
from sqlalchemy.exc import SQLAlchemyError

from database.database import async_session_maker
from models.post_models import Post
from models.user_models import User

from .base import BaseDAO


class PostDAO(BaseDAO):
    model = Post

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            try:
                query = (
                    select(cls.model.__table__.columns, User.username)
                    .filter_by(**filter_by)
                    .join(User, cls.model.user_id == User.id)
                )
                result = await session.execute(query)
                return result.mappings().one_or_none()
            except (SQLAlchemyError, Exception) as e:
                logger.error('Ошибка при поиске записи в бд', extra={'данные': filter_by})
                return None

    @classmethod
    async def find_all(cls, category: str | None = None,  text: str | None = None, **filter_by):
        async with async_session_maker() as session:
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
                logger.error('Ошибка при поиске записей в бд', extra={'данные': filter_by})
                return None

    @classmethod
    async def search_post(cls, text: str):
        async with async_session_maker() as session:
            try:
                query = (
                select(cls.model.__table__.columns, User.username)
                .where(cls.model.title.icontains(text))
                .join(User, cls.model.user_id == User.id)
                )
                res = await session.execute(query)
                return res.mappings().all()
            except (SQLAlchemyError, Exception) as e:
                logger.error('Ошибка при поиске записей в бд', extra={'данные': text})
                return None


    @classmethod
    async def update_post(cls, user_id: int, post_id: int, **data):
        async with async_session_maker() as session:
            try:
                query = (
                update(cls.model)
                .where(and_(cls.model.id == post_id, cls.model.user_id == user_id))
                .values(**data).returning(cls.model)
                )
                await session.execute(query)
                await session.commit()
            except (SQLAlchemyError, Exception) as e:
                logger.error('Ошибка при поиске записей в бд', 
                            extra={'данные': {'user_id': user_id,
                                                'post_id': post_id, 'data': data}})
                return None
    
    @classmethod
    async def like_post(cls, post_id: int, **data):
        async with async_session_maker() as session:
            try:
                query = (
                update(cls.model)
                .where(cls.model.id == post_id)
                .values(**data).returning(cls.model)
                )
                await session.execute(query)
                await session.commit()
            except (SQLAlchemyError, Exception) as e:
                logger.error('Ошибка при добавлении лайка на запись', extra={'данные': {'post_id': post_id, 'data': data}})
                return None