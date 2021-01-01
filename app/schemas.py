from typing import List, ForwardRef

from pydantic import BaseModel, EmailStr, Field

UserPost = ForwardRef('Post')


class Post(BaseModel):
    owner_id: int
    title: str
    description: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr = Field(None, example="user@example.com", title="User email")


class User(UserBase):
    name: str
    password: str

    class Config:
        orm_mode = True


class UserGet(UserBase):
    name: str
    posts: List[Post] = []

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    name: str
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class PostUser(UserBase):
    name: str

    class Config:
        orm_mode = True


class PostGet(BaseModel):
    owner_id: int
    title: str
    description: str

    owner: PostUser

    class Config:
        orm_mode = True


class PostDelete(BaseModel):
    message: str

    class Config:
        orm_mode = True
