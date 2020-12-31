from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Post as PostModel
from app import schemas

router = APIRouter()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/posts/", response_model=List[schemas.PostGet])
def get_posts(database: Session = Depends(get_db)):
    users = database.query(PostModel).all()
    return users


@router.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    db_post = PostModel(owner_id=post.owner_id, title=post.title, description=post.description)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/posts/{id}/", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.put("/posts/{id}/", response_model=schemas.Post)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    pass

# @router.post("/user/", response_model=SchemaUser)
# async def create_user(user: SchemaUser):
#     db_user = ModelUser(
#         first_name=user.first_name, last_name=user.last_name, age=user.age
#     )
#     db.session.add(db_user)
#     db.session.commit()
#     return db_user
