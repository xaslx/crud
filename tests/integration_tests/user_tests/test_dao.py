import pytest
from pydantic import EmailStr

from dao.users_dao import UsersDAO


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "id, email, exist",
    [
        (1, "dasha@example.com", True),
        (2, "knyazev@gmail.com", True),
        (3, None, False),
    ],
)
async def test_find_one_or_none_user(id: int, email: EmailStr, exist: bool):
    user = await UsersDAO.find_one_or_none(id=id)
    if exist:
        assert user
        assert user.email == email
    else:
        assert not user


@pytest.mark.asyncio
async def test_find_all_user():
    users = await UsersDAO.find_all()
    assert len(users) == 2


@pytest.mark.asyncio
async def test_update_user():
    await UsersDAO.update_user(user_id=1, username="maksim")
    user = await UsersDAO.find_one_or_none(id=1)
    assert user.username == "maksim"
