from datetime import datetime, timedelta

from fastapi import HTTPException
from jwt import PyJWTError
from sqlalchemy.orm import Session, joinedload
from starlette.status import HTTP_401_UNAUTHORIZED

from app import schemas, models


def create_comment(db: Session, comment: schemas.CommentCreate, current_user):
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    new_comment = models.Comment(
        comment=comment.comment, owner_id=current_user.id, post_id=comment.post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def all_comments(db: Session):
    return db.query(models.Comment).options(joinedload(models.Comment.owner)).all()


def get_comments_by_post(db: Session, post_id):
    return db.query(models.Comment).options(joinedload(models.Comment.owner)).filter(models.Comment.post_id == post_id).all()


def get_comments_by_user(db: Session, current_user):
    return db.query(models.Comment).options(joinedload(models.Comment.owner)).filter(models.Comment.owner_id == current_user.id).all()
