from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from .base import get_db
from app.models import Post as PostModel
from app import schemas

router = APIRouter()


@router.get("/posts/", response_model=List[schemas.PostGet])
def get_posts(database: Session = Depends(get_db)):
    """
        Get all posts
    """
    users = database.query(PostModel).all()
    return users


@router.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    """
        Create new post
    """
    db_post = PostModel(owner_id=post.owner_id, title=post.title, description=post.description)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/posts/{id}/", response_model=schemas.PostGet)
def get_post(id: int, db: Session = Depends(get_db)):
    """
        Get single post
    """
    # options() to get related model
    post = db.query(PostModel).options(joinedload(PostModel.owner)).filter(PostModel.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.put("/posts/{id}/", response_model=schemas.Post)
def update_post(id: int, post_data: schemas.Post, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = post_data.title
    post.description = post_data.description
    db.commit()
    db.refresh(post)
    return post


@router.delete("/posts/{id}/", response_model=schemas.PostDelete)
def delete_post(id: int, db: Session = Depends(get_db)):
    """
        Delete post by id
    """
    post = db.query(PostModel).filter(PostModel.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}

# @router.post("/user/", response_model=SchemaUser)
# async def create_user(user: SchemaUser):
#     db_user = ModelUser(
#         first_name=user.first_name, last_name=user.last_name, age=user.age
#     )
#     db.session.add(db_user)
#     db.session.commit()
#     return db_user
