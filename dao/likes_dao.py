from dao.base import BaseDAO
from models.like_models import Like
from database.database import async_session_maker
from sqlalchemy import select
from models.post_models import Post
from logger import logger
from sqlalchemy.exc import SQLAlchemyError


class LikeDAO(BaseDAO):
    model = Like


    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            try:
                query = (
                    select(cls.model.__table__.columns, Post.title)
                    .filter_by(**filter_by)
                    .join(Post, cls.model.post_id == Post.id)
                )
                result = await session.execute(query)
                return result.mappings().all()
            except (SQLAlchemyError, Exception) as e:
                logger.error('Ошибка при поиске значений', extra={'данные': filter_by})
                return None