# Dependency
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud, models
from app.api.user import get_current_user
from app.database import SessionLocal

router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/comments/", response_model=schemas.CommentCreate)
def create_comment(comment_data: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
        add new comment

        - **post_id**: Post ID
        - **comment**: User comment
    """
    return crud.create_comment(db, comment_data, current_user)


@router.get("/comments/", response_model=List[schemas.CommentList])
def get_comments(db: Session = Depends(get_db)):
    return crud.all_comments(db)


@router.get("/comments/{post_id}", response_model=List[schemas.CommentList])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    return crud.get_comments_by_post(db, post_id)


@router.get("/my-comments/", response_model=List[schemas.CommentList])
def get_comments_for_current_user(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_comments_by_user(db, current_user)
