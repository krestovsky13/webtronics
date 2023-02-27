from pydantic import BaseModel
from datetime import date

from apps.users.schemas import ShowUser


class PostBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    author_id: int


class ShowPost(PostBase):
    title: str
    description: str
    author: ShowUser
    like_count: int
    created_at: date
