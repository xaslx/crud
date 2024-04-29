from pydantic import BaseModel, ConfigDict


class Like(BaseModel):
    user_id: int
    post_id: int
    post_title: str

    model_config = ConfigDict(from_attributes=True)
