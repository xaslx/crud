from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .users_schemas import UserShort


class CommentIn(BaseModel):
    text: str = Field(max_length=300, min_length=1)


class CommentOut(CommentIn):
    created_at: datetime
    user: UserShort

    model_config = ConfigDict(from_attributes=True)
