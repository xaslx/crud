from sqlalchemy import insert, select, update

from database.database import async_session_maker
from models.user_models import User

from .base import BaseDAO


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__.columns)
                .filter_by(**filter_by)
                .order_by(cls.model.__table__.columns.registered_at)
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def update_user(cls, user_id: int, **data):
        query = update(cls.model).where(cls.model.id == user_id).values(**data)
        async with async_session_maker() as session:
            await session.execute(query)
            await session.commit()
