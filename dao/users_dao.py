from sqlalchemy import insert, select, update

from database.database import async_session_maker
from models.user_models import User
from logger import logger
from sqlalchemy.exc import SQLAlchemyError
from .base import BaseDAO


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            try:
                query = (
                    select(cls.model.__table__.columns)
                    .filter_by(**filter_by)
                    .order_by(cls.model.__table__.columns.registered_at)
                )
                result = await session.execute(query)
                return result.mappings().all()
            except (SQLAlchemyError, Exception) as e:
                logger.error('Ошибка при поиске значений', extra={'данные': filter_by})
                return None

    @classmethod
    async def update_user(cls, user_id: int, **data):
        async with async_session_maker() as session:
            try:
                query = update(cls.model).where(cls.model.id == user_id).values(**data)
                await session.execute(query)
                await session.commit()
            except (SQLAlchemyError, Exception) as e:
                logger.error('Ошибка при обновлении пользователя', extra={'данные': {'user_id': user_id, 'data': data}})
                return None
