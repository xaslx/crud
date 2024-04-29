import pytest
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from repository.users_repository import UsersRepository

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "id, email, exist",
    [
        (1, "dasha@example.com", True),
        (2, "knyazev@gmail.com", True),
        (3, None, False),
    ],
)
async def test_find_one_or_none_user(
    id: int, email: EmailStr, exist: bool, session: AsyncSession
):
    user = await UsersRepository.find_one_or_none(id=id, session=session)
    if exist:
        assert user
        assert user.email == email
    else:
        assert not user


@pytest.mark.asyncio
async def test_find_all_user(session: AsyncSession):
    users = await UsersRepository.find_all(session=session)
    assert len(users) == 2


@pytest.mark.asyncio
async def test_update_user(session: AsyncSession):
    await UsersRepository.update_user(
        user_id=1, username="maksim", session=session
    )
    user = await UsersRepository.find_one_or_none(id=1, session=session)
    assert user.username == "maksim"
