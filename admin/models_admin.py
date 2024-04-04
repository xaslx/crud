from sqladmin import ModelView

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
    ]
    can_delete = False
    icon = "fa-solid fa-user"


class PostAdmin(ModelView, model=Post):
    name = "Пост"
    name_plural = "Посты"
    column_list = "__all__"
    icon = "fa-solid fa-pencil-square"
