from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi_cache.decorator import cache
from fastapi_pagination import Page, paginate

from auth.dependencies import get_admin_user, get_current_user
from dao.posts_dao import PostDAO
from dao.users_dao import UsersDAO
from exceptions import PostNotDeleted, PostNotFound, UserNotFound
from models.user_models import User
from schemas.posts_schemas import (
    Category,
    Posts,
    PostsIn,
    PostsIn2,
)

template = Jinja2Templates("templates")

router = APIRouter(prefix="/posts", tags=["Посты"])


@router.get("")
@cache(expire=60)
async def get_all_posts(
    category: Annotated[Category, Query()] = None
) -> Page[Posts]:
    posts = await PostDAO.find_all_join(category=category)
    return paginate(posts)


@router.get("/users/{username}")
async def posts_by_username(
    username: str, category: Annotated[Category, Query()] = None
) -> Page[Posts]:
    user = await UsersDAO.find_one_or_none(username=username)
    if not user:
        raise UserNotFound
    posts = await PostDAO.find_all_join(category=category, user_id=user.id)
    return paginate(posts)


@router.get("/me")
async def find_my_posts(
    user: User = Depends(get_current_user),
    category: Annotated[Category, Query()] = None,
) -> Page[Posts]:
    posts = await PostDAO.find_all_join(category=category, user_id=user.id)
    return paginate(posts)


@router.get("/{post_id}")
async def find_post_by_id(post_id: int, request: Request) -> Posts:
    post = await PostDAO.find_one_or_none(id=post_id)
    if not post:
        raise PostNotFound
    return post


@router.post("")
async def add_new_post(
    post: PostsIn, category: Category, user: User = Depends(get_current_user)
):
    if not user:
        raise UserNotFound
    return await PostDAO.add(
        title=post.title,
        user_id=user.id,
        content=post.content,
        category=category.value,
    )


@router.delete("/{post_id}")
async def delete_post(post_id: int, user: User = Depends(get_current_user)):
    post = await PostDAO.find_one_or_none(id=post_id)
    if not post:
        raise PostNotFound
    if post.user_id != user.id:
        raise PostNotDeleted
    return await PostDAO.delete(id=post_id)


@router.delete("/admin/{post_id}")
async def delete_post(post_id: int, user: User = Depends(get_admin_user)):
    return await PostDAO.delete(id=post_id)


@router.put("/{post_id}")
async def update_post(post: PostsIn2, user: User = Depends(get_current_user)):
    user_post = await PostDAO.find_one_or_none(user_id=user.id)
    if not user_post:
        raise PostNotFound
    else:
        new_title = post.title
        new_content = post.content
        return await PostDAO.update_post(
            user_id=user.id,
            post_id=post.post_id,
            title=new_title,
            date_of_update=datetime.utcnow(),
            content=new_content,
        )
