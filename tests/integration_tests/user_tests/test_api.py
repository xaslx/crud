import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, email, password, status_code",
    [
        ("earth", "earth@gmail.com", "afeafaegae", 409),
        (123456, "jkafagrr@gmail.com", "afeafaegae", 422),
        ("123456", "jkafagrr@gmail.com", 1651651563, 422),
        ("anton", "anton@gmail.com", "anton", 409),
        ("melissa", "melissa@gmail.com", "melisaa", 409),
        ("admin", "admin@mail.ru", "admins", 200),
        ("admin", "admin@mail.ru", "admins", 409),
        ("admin2", "admin@mail.ru", "admins", 409),
        ("admin", "admin@mail.ruU", "admins", 409),
        ("русский", "example@mail.ru", "admins", 422),
        ("example", "example2@mail.ru", "русский", 422),
        ("example$%2", "example3@mail.ru", "tesstt", 422),
        ("example3", "example4@mail.ru", "%$#@&!test", 422),
        (
            "exampleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
            "example5@mail.ru",
            "2023-05-01",
            "tesstt",
            422,
        ),
        (
            "example5",
            "example6@mail.ru",
            "2023-05-01",
            "tessttttttttttttttttttttttttttttttttttttttttttttttttttttttt",
            422,
        ),
    ],
)
async def test_register_user(
    username, email, password, status_code, ac: AsyncClient
):
    response = await ac.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code


@pytest.mark.acyncio
@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ("dasha", "string", 200),
        ("maks4on", "string", 200),
        ("Dmitriy", "string", 401),
    ],
)
async def test_login_user(username, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/login", json={"username": username, "password": password}
    )

    assert response.status_code == status_code
