from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_cache.decorator import cache
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_admin_user, get_current_user
from database.database import get_async_session
from exceptions import (
    NotAccess,
    PostNotFound,
    UnverifiedUser,
    UserNotFound,
    YourAccountIsBlocked,
)
from logger import logger
from models.user_models import User
from repository.comments_repository import CommentRepository
from repository.posts_repository import PostRepository
from repository.users_repository import UsersRepository
from schemas.comments_schemas import CommentIn
from schemas.posts_schemas import (
    Category,
    MyPosts,
    Posts,
    PostsIn,
    PostWComments,
)

template = Jinja2Templates("templates")

router = APIRouter(prefix="/posts", tags=["Посты"])


@router.post("/add_post")
async def add_new_post(
    post: PostsIn,
    user: User = Depends(get_current_user),
    async_db: AsyncSession = Depends(get_async_session),
):
    if not user:
        raise UserNotFound
    if not user.is_verified:
        raise UnverifiedUser
    if user.is_banned:
        raise YourAccountIsBlocked
    logger.info(
        f"Пользователь {user.username} добавил новый пост {post.title}"
    )
    post = await PostRepository.add(
        title=post.title,
        user_id=user.id,
        content=post.content,
        category=post.category.value,
        session=async_db,
    )
    logger.info(
        f"Пользователь {user.username} добавил новый пост {post.title}"
    )
    return post


@router.get("")
@cache(expire=30)
async def get_all_posts(
    category: Annotated[str, Query()] = None,
    async_db: AsyncSession = Depends(get_async_session),
) -> list[Posts]:
    posts = await PostRepository.find_all(session=async_db, category=category)
    return posts


@router.get("/search")
async def search_post(
    text: Annotated[str, Query()] = None,
    async_db: AsyncSession = Depends(get_async_session),
) -> list[Posts]:
    if not text:
        return JSONResponse(content={"msg": "Пустой запрос"})
    posts = await PostRepository.search_post(text=text, session=async_db)
    return posts


@router.get("/users/{username}")
async def posts_by_username(
    username: str,
    category: Annotated[Category, Query()] = None,
    async_db: AsyncSession = Depends(get_async_session),
) -> Page[Posts]:
    user = await UsersRepository.find_one_or_none(
        username=username, session=async_db
    )
    if not user:
        raise UserNotFound
    posts = await PostRepository.find_all(
        session=async_db, user_id=user.id, category=category
    )
    return paginate(posts)


@router.get("/me")
async def find_my_posts(
    user: User = Depends(get_current_user),
    category: Annotated[Category, Query()] = None,
    async_db: AsyncSession = Depends(get_async_session),
) -> Page[MyPosts]:

    posts = await PostRepository.find_all(
        session=async_db, user_id=user.id, category=category
    )
    return paginate(posts)


@router.get("/{post_id}")
async def find_post_by_id(
    post_id: int, async_db: AsyncSession = Depends(get_async_session)
) -> PostWComments:
    post = await PostRepository.find_one_or_none_and_comments(
        id=post_id, session=async_db
    )
    if not post:
        raise PostNotFound
    return post


@router.post("/comments/{post_id}")
async def add_comment(
    post_id: int,
    comment: CommentIn,
    user: User = Depends(get_current_user),
    async_db: AsyncSession = Depends(get_async_session),
):
    post = await PostRepository.find_one_or_none(id=post_id, session=async_db)
    if not post:
        raise PostNotFound
    return await CommentRepository.add(
        user_id=user.id, post_id=post.id, text=comment.text, session=async_db
    )


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    user: User = Depends(get_current_user),
    async_db: AsyncSession = Depends(get_async_session),
):
    post = await PostRepository.find_one_or_none(id=post_id, session=async_db)
    if not post:
        raise PostNotFound
    if post.user_id != user.id:
        raise NotAccess
    deleted = await PostRepository.delete(id=post_id, session=async_db)
    logger.info(f"Пользователь {user.username} удалил пост {post.id}")
    return deleted


@router.delete("/admin/{post_id}")
async def delete_post_admin(
    post_id: int,
    user: User = Depends(get_admin_user),
    async_db: AsyncSession = Depends(get_async_session),
):

    deleted = await PostRepository.delete(id=post_id, session=async_db)
    logger.info(f"Администратор {user.username} удалил пост {post_id}")
    return deleted


@router.put("/{post_id}")
async def update_post(
    post_id: int,
    post: PostsIn,
    user: User = Depends(get_current_user),
    async_db: AsyncSession = Depends(get_async_session),
):
    user_post = await PostRepository.find_one_or_none(
        id=post_id, session=async_db
    )
    if not user_post:
        raise PostNotFound
    if user_post.user_id != user.id:
        raise NotAccess
    else:
        updated_post = await PostRepository.update_post(
            post_id=post_id,
            user_id=user.id,
            title=post.title,
            date_of_update=datetime.utcnow(),
            content=post.content,
            category=post.category.value,
            session=async_db,
        )
        logger.info(
            f"Пользователь {user.username} обновил пост {user_post.id}"
        )
        return updated_post
