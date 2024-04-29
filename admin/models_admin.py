from sqladmin import ModelView

from models.comments_models import Comment
from models.post_models import Post
from models.user_models import User


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    column_details_exclude_list = [User.hashed_password]
    column_list = [
        User.id,
        User.username,
        User.email,
        User.role,
        User.registered_at,
        User.is_verified,
        User.is_banned,
    ]
    can_delete = False
    icon = "fa-solid fa-user"
    column_searchable_list = [User.id, User.username, User.email]
    column_sortable_list = [User.registered_at]


class PostAdmin(ModelView, model=Post):
    name = "Пост"
    name_plural = "Посты"
    column_list = [
        Post.id,
        Post.user_id,
        Post.date_of_publication,
        Post.date_of_update,
        Post.likes,
        Post.title,
        Post.content,
        Post.category,
        Post.comments,
    ]
    column_searchable_list = [Post.title, Post.id]
    column_formatters = {Post.comments: lambda x, a: x.comments[:3]}
    icon = "fa-solid fa-pencil-square"
    column_sortable_list = [Post.date_of_publication]
    column_details_list = [Post.title]


class CommentAdmin(ModelView, model=Comment):
    name = "Комментарий"
    name_plural = "Комментарии"
    column_list = "__all__"
    icon = "fa-solid fa-comments"
    column_searchable_list = [Comment.id, Comment.user_id, Comment.post_id]
    column_sortable_list = [Comment.created_at]
