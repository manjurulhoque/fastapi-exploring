from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User as UserModel
from app import schemas

router = APIRouter()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/users/", response_model=List[schemas.User])
def get_users(database: Session = Depends(get_db)):
    users = database.query(UserModel).all()
    return users


@router.post("/users/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    fake_hashed_password = user.password + "not_really_hashed"
    db_user = UserModel(email=user.email, password=fake_hashed_password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# @router.post("/user/", response_model=SchemaUser)
# async def create_user(user: SchemaUser):
#     db_user = ModelUser(
#         first_name=user.first_name, last_name=user.last_name, age=user.age
#     )
#     db.session.add(db_user)
#     db.session.commit()
#     return db_user
