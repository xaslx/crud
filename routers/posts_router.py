from datetime import datetime
from typing import Annotated
from random import choice
from fastapi import APIRouter, Depends, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
from fastapi_pagination import Page, paginate
from auth.dependencies import get_admin_user, get_current_user
from dao.posts_dao import PostDAO
from dao.users_dao import UsersDAO
from exceptions import PostNotDeleted, PostNotFound, UserNotFound, UnverifiedUser, NotAccess
from models.user_models import User
from schemas.posts_schemas import (
    Category,
    Posts,
    PostsIn,
    MyPosts
)

template = Jinja2Templates("templates")

router = APIRouter(prefix="/posts", tags=["Посты"])


@router.get("")
@cache(expire=60)
async def get_all_posts(category: Annotated[Category, Query()] = None) -> Page[Posts]:
    posts = await PostDAO.find_all(category=category)
    return paginate(posts)



@router.get('/search')
async def search_post(text: Annotated[str, Query()] = None):
    if not text:
        return JSONResponse(content={'msg': 'Пустой запрос'})
    return await PostDAO.search_post(text=text)


@router.get("/users/{username}")
async def posts_by_username(
    username: str, category: Annotated[Category, Query()] = None
) -> Page[Posts]:
    user = await UsersDAO.find_one_or_none(username=username)
    if not user:
        raise UserNotFound
    posts = await PostDAO.find_all(user_id=user.id, category=category)
    return paginate(posts)


@router.get("/me")
async def find_my_posts(
    user: User = Depends(get_current_user),
    category: Annotated[Category, Query()] = None,) -> Page[MyPosts]:
    posts = await PostDAO.find_all(user_id=user.id, category=category)
    return paginate(posts)


@router.get("/{post_id}")
async def find_post_by_id(post_id: int, request: Request) -> Posts:
    post = await PostDAO.find_one_or_none(id=post_id)
    if not post:
        raise PostNotFound
    return post


@router.post("/add_post")
async def add_new_post(
    post: PostsIn, category: Category, user: User = Depends(get_current_user)
):
    if not user:
        raise UserNotFound
    if not user.is_verified:
        raise UnverifiedUser
    return await PostDAO.add(
        title=post.title,
        user_id=user.id,
        content=post.content,
        category=category
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
async def update_post(post_id: int, post: PostsIn, user: User = Depends(get_current_user)):
    user_post = await PostDAO.find_one_or_none(id=post_id)
    if not user_post:
        raise PostNotFound
    if user_post.user_id != user.id:
        raise NotAccess
    else:
        return await PostDAO.update_post(
            post_id=post_id,
            user_id=user.id,
            title=post.title,
            date_of_update=datetime.utcnow(),
            content=post.content,
        )
