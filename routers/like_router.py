from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from database.database import get_async_session
from exceptions import PostNotFound
from logger import logger
from models.user_models import User
from repository.likes_repository import LikeRepository
from repository.posts_repository import PostRepository
from schemas.likes_schemas import Like

router = APIRouter(prefix="/like", tags=["Лайки"])


@router.post("/{post_id}")
async def like_it(
    post_id: int,
    user: User = Depends(get_current_user),
    async_db: AsyncSession = Depends(get_async_session),
):
    like = await LikeRepository.find_one_or_none(
        post_id=post_id, user_id=user.id, session=async_db
    )
    post = await PostRepository.find_one_or_none(id=post_id, session=async_db)
    if not post:
        raise PostNotFound
    if not like:
        await LikeRepository.add(
            post_id=post_id, user_id=user.id, session=async_db
        )
        logger.info(
            f"Пользователь {user.username} поставил лайк на пост - {post.id}"
        )
        return await PostRepository.like_post(
            post_id=post_id, session=async_db, likes=post.likes + 1
        )
    await LikeRepository.delete(
        post_id=post_id, user_id=user.id, session=async_db
    )
    logger.info(f"Пользователь {user.username} убрал лайк на пост - {post.id}")
    return await PostRepository.like_post(
        post_id=post_id, session=async_db, likes=post.likes - 1
    )


@router.get("/my_liked_posts")
async def get_my_liked_posts(
    user: User = Depends(get_current_user),
    async_db: AsyncSession = Depends(get_async_session),
) -> Page[Like]:
    posts = await LikeRepository.find_all(user_id=user.id, session=async_db)
    return paginate(posts)
