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
        (
            "",
            "Простой тестПростой тест Простой тестПростой тест",
            1,
            "Спорт",
            422,
        ),
        ("Простой тест", "", 1, "Спорт", 422),
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
        "/posts/add_post",
        json={
            "title": title,
            "content": content,
            "user_id": user_id,
            "category": category,
        },
    )
    assert response.status_code == status_code


@pytest.mark.acyncio
@pytest.mark.parametrize(
    "text, user_id, post_id, status_code",
    [("Тестовый комментарий", 1, 1, 200), ("", 1, 1, 422)],
)
async def test_add_comment(
    text: str,
    user_id: int,
    post_id: int,
    status_code: int,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        f"/posts/comments/{post_id}",
        json={"text": text, "user_id": user_id, "post_id": post_id},
    )
    assert response.status_code == status_code


@pytest.mark.asyncio
@pytest.mark.parametrize("post_id, status_code", [(2, 200)])
async def test_delete_post(
    post_id, status_code, authenticated_ac: AsyncClient
):
    response = await authenticated_ac.delete(
        f"/posts/admin/{post_id}",
    )
    assert response.status_code == status_code
