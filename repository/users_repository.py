from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from logger import logger
from models.user_models import User

from .base_repository import BaseRepository


class UsersRepository(BaseRepository):
    model = User

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        try:
            query = (
                select(cls.model.__table__.columns)
                .filter_by(**filter_by)
                .order_by(cls.model.__table__.columns.registered_at)
            )
            result = await session.execute(query)
            return result.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                "Ошибка при поиске значений", extra={"данные": filter_by}
            )
            return None

    @classmethod
    async def update_user(cls, user_id: int, session: AsyncSession, **data):
        try:
            query = (
                update(cls.model).where(cls.model.id == user_id).values(**data)
            )
            await session.execute(query)
            await session.commit()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                "Ошибка при обновлении пользователя",
                extra={"данные": {"user_id": user_id, "data": data}},
            )
            return None
