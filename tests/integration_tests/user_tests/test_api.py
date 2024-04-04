import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, email, date_of_birthday, password, status_code",
    [
        ("earth", "earth@gmail.com", "2025-05-06", "afeafaegae", 409),
        (123456, "jkafagrr@gmail.com", "2023-01-01", "afeafaegae", 422),
        ("123456", "jkafagrr@gmail.com", "2023-01-01", 1651651563, 422),
        ("anton", "anton@gmail.com", "2099-01-01", "anton", 409),
        ("melissa", "melissa@gmail.com", "1899-01-01", "melisaa", 409),
        ("admin", "admin@mail.ru", "2023-01-01", "admins", 200),
        ("admin", "admin@mail.ru", "2023-05-01", "admins", 409),
        ("admin2", "admin@mail.ru", "2023-05-01", "admins", 409),
        ("admin", "admin@mail.ruU", "2023-05-01", "admins", 409),
        ("русский", "example@mail.ru", "2023-05-01", "admins", 422),
        ("example", "example2@mail.ru", "2023-05-01", "русский", 422),
        ("example$%2", "example3@mail.ru", "2023-05-01", "tesstt", 422),
        ("example3", "example4@mail.ru", "2023-05-01", "%$#@&!test", 422),
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
    username, email, date_of_birthday, password, status_code, ac: AsyncClient
):
    response = await ac.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "date_of_birthday": date_of_birthday,
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
