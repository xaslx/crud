import pytest
from httpx import AsyncClient


@pytest.mark.acyncio
@pytest.mark.parametrize(
    "title, content, user_id, category, status_code",
    [
        (
            "Простой тест",
            "Простой тестПростой тест Простой тестПростой тест",
            1,
            "Спорт",
            200,
        ),
    ],
)
async def test_add_new_post(
    title,
    content,
    user_id,
    category,
    status_code,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "/posts",
        json={
            "title": title,
            "content": content,
            "user_id": user_id,
            "category": category,
        },
    )
    assert response.status_code == status_code


@pytest.mark.acyncio
@pytest.mark.parametrize("post_id, status_code", [(1, 200)])
async def test_delete_post(
    post_id, status_code, authenticated_ac: AsyncClient
):
    response = await authenticated_ac.delete(
        f"/posts/{post_id}",
        params={
            "post_id": post_id,
        },
    )
    assert response.status_code == status_code
