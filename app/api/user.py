from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from app import schemas, crud, models
from .base import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get("/users/", response_model=List[schemas.User])
def get_users(database: Session = Depends(get_db)):
    users = crud.get_users(database)
    return users


@router.post("/signup/", response_model=schemas.UserCreate)
def signup(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """add new user"""
    user = crud.get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=409, detail="Email already exists.")
    new_user = crud.create_user(db, user_data)
    return new_user


@router.post("/login/", response_model=schemas.Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """generate access token for valid credentials"""
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=60)
    access_token = crud.create_access_token(data={"sub": user.email},
                                            expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return crud.decode_access_token(db, token)
    # credentials_exception = HTTPException(
    #     status_code=HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    # try:
    #     payload = jwt.decode(token, "secret", algorithms=["HS256"])
    #     email: str = payload.get("email")
    #
    #     if email is None:
    #         raise credentials_exception
    #
    # except PyJWTError:
    #     raise credentials_exception
    #
    # user = crud.get_user_by_email(db, email)
    #
    # if user is None:
    #     raise credentials_exception
    #
    # return user


@router.get("/me/", response_model=schemas.UserGet)
def read_logged_in_user(current_user: models.User = Depends(get_current_user)):
    """return user settings for current user"""
    return current_user


@router.get("/refresh_token")
async def get_refresh_token(refresh_token: str):
    """ Take an existing refresh token for a new JWT token, client stores refresh token """
    pass


@router.get("/myposts/", response_model=List[schemas.Post])
def get_own_posts(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """return a list of Posts owned by current user"""
    posts = crud.get_user_posts(db, current_user.id)
    return posts

# @router.post("/users/", response_model=schemas.UserCreate)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     fake_hashed_password = user.password + "not_really_hashed"
#     db_user = UserModel(email=user.email, password=fake_hashed_password, name=user.name)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @router.post("/user/", response_model=SchemaUser)
# async def create_user(user: SchemaUser):
#     db_user = ModelUser(
#         first_name=user.first_name, last_name=user.last_name, age=user.age
#     )
#     db.session.add(db_user)
#     db.session.commit()
#     return db_user
