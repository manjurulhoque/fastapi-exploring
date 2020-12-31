from typing import List, ForwardRef

from pydantic import BaseModel

UserPost = ForwardRef('Post')


class Post(BaseModel):
    owner_id: int
    title: str
    description: str

    class Config:
        orm_mode = True


class PostGet(BaseModel):
    owner_id: int
    title: str
    description: str

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str

    posts: List[Post] = []

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True
