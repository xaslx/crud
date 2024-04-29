import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from repository.posts_repository import PostRepository


@pytest.mark.asyncio
async def test_add_and_get_post_and_delete(session: AsyncSession):
    await PostRepository.add(
        user_id=1,
        title="TestTest",
        content="TestTestTestTest",
        category="Спорт",
        session=session,
    )
    post = await PostRepository.find_one_or_none(id=3, session=session)
    assert post
    await PostRepository.delete(id=3, session=session)
    post = await PostRepository.find_one_or_none(id=3, session=session)
    assert not post


@pytest.mark.asyncio
async def test_update_post(session: AsyncSession):
    post = await PostRepository.find_one_or_none(id=1, session=session)
    assert post.title == "Новый пост"
    await PostRepository.update_post(
        user_id=1, post_id=1, title="TEST_TEST", session=session
    )
    post = await PostRepository.find_one_or_none(id=1, session=session)
    assert post.title == "TEST_TEST"


@pytest.mark.asyncio
async def test_find_post_by_id(session: AsyncSession):
    post = await PostRepository.find_one_or_none(id=1, session=session)
    assert post


@pytest.mark.asyncio
async def test_search_post(session: AsyncSession):
    text = "python"
    res = await PostRepository.search_post(text=text, session=session)
    assert len(res) == 2
