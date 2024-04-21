from fastapi.responses import JSONResponse
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError
from database.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        # async with async_session_maker() as session:
        #     query = insert(cls.model).values(**data).returning(cls.model)
        #     result = await session.execute(query)
        #     await session.commit()
        #     return result.scalar()
        try:
            query = insert(cls.model).values(**data).returning(cls.model)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.scalar()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Ошибка в бд: Не удалось добавить данные в бд"
            elif isinstance(e, Exception):
                msg = "Неизвестная ошибка: Не удалось добавить данные в бд"
            return None

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
            return JSONResponse(content={"msg": "Удалено"})
