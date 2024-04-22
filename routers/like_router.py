from fastapi import APIRouter, Depends
from dao.likes_dao import LikeDAO
from dao.posts_dao import PostDAO
from auth.dependencies import get_current_user
from exceptions import PostNotFound
from models.user_models import User
from fastapi_pagination import Page, paginate
from schemas.likes_schemas import Like
from models.post_models import Post
from logger import logger



router = APIRouter(
    prefix='/like',
    tags=['Лайки']
)



@router.post('/{post_id}')
async def like_it(post_id: int, user: User = Depends(get_current_user)):
    like = await LikeDAO.add(post_id=post_id, user_id=user.id)
    post: Post = await PostDAO.find_one_or_none(id=post_id)
    if not post:
        raise PostNotFound
    if like:
        logger.info(f'Пользователь {user.username} поставил лайк на пост - {post.id}')
        return await PostDAO.like_post(post_id=post_id, likes=post.likes + 1)
    await LikeDAO.delete(post_id=post_id, user_id=user.id)
    logger.info(f'Пользователь {user.username} убрал лайк на пост - {post.id}')
    return await PostDAO.like_post(post_id=post_id, likes=post.likes - 1)

@router.get('/my_liked_posts')
async def get_my_liked_posts(user: User = Depends(get_current_user)) -> Page[Like]:
    posts = await LikeDAO.find_all(user_id=user.id)
    return paginate(posts)