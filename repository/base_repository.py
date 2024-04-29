from fastapi.responses import JSONResponse
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import async_session_maker
from logger import logger


class BaseRepository:
    model = None

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        try:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                "Ошибка при поиске значения", extra={"данные": filter_by}
            )
            return None

    @classmethod
    async def find_one_or_none_for_admin(cls, **filter_by):
        async with async_session_maker() as session:
            try:
                query = select(cls.model.__table__.columns).filter_by(
                    **filter_by
                )
                result = await session.execute(query)
                return result.mappings().one_or_none()
            except (SQLAlchemyError, Exception) as e:
                logger.error(
                    "Ошибка при поиске значения", extra={"данные": filter_by}
                )
                return None

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        try:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                "Ошибка при поиске значений", extra={"данные": filter_by}
            )
            return None

    @classmethod
    async def add(cls, session: AsyncSession, **data):
        try:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Ошибка в бд: Не удалось добавить данные в бд"
            elif isinstance(e, Exception):
                msg = "Неизвестная ошибка: Не удалось добавить данные в бд"
            logger.error(msg, extra={"данные": data})
            return None

    @classmethod
    async def delete(cls, session: AsyncSession, **filter_by):
        try:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
            return JSONResponse(content={"msg": "Удалено"})
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Ошибка в бд: Не удалось добавить данные в бд"
            elif isinstance(e, Exception):
                msg = "Неизвестная ошибка: Не удалось добавить данные в бд"
            logger.error(msg, extra={"данныые": filter_by})
            return None
