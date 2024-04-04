import pytest

from dao.posts_dao import PostDAO


@pytest.mark.asyncio
async def test_add_and_get_post_and_delete():
    await PostDAO.add(
        user_id=1,
        title="TestTest",
        content="TestTestTestTest",
        category="Спорт",
    )
    post = await PostDAO.find_one_or_none(id=3)
    assert post
    await PostDAO.delete(id=3)
    post = await PostDAO.find_one_or_none(id=3)
    assert not post


@pytest.mark.asyncio
async def test_update_post():
    post = await PostDAO.find_one_or_none(id=1)
    assert post.title == "NEW POST"
    await PostDAO.update_post(user_id=1, post_id=1, title="TEST_TEST")
    post = await PostDAO.find_one_or_none(id=1)
    assert post.title == "TEST_TEST"


@pytest.mark.asyncio
async def test_find_post_by_id():
    post = await PostDAO.find_one_or_none(id=1)
    assert post
