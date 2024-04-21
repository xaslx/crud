from pydantic import BaseModel
from .posts_schemas import MyPosts


class Like(BaseModel):
    user_id: int
    post_id: int
    title: str