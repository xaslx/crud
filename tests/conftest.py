import asyncio
import json

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from config.config import settings
from database.database import Base, async_session_maker, engine
from main import app
from models.post_models import Post
from models.user_models import User


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock(model: str):
        with open(f"tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock("users")
    posts = open_mock("posts")

    async with async_session_maker() as session:
        for Model, values in [(User, users), (Post, posts)]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        await ac.post(
            "/auth/login", json={"username": "maksss", "password": "string"}
        )
        print(ac.cookies)
        assert ac.cookies["user_access_token"]
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
