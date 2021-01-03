from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    posts = relationship("Post", back_populates="owner", lazy=True)
    comments = relationship("Comment", back_populates="owner", lazy=True)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String)
    description = Column(Text)

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", lazy=True)

    def __repr__(self):
        return f"<Post(title='{self.title}', description='{self.description}')>"


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    comment = Column(Text)

    owner = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
