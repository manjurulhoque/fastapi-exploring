from fastapi import APIRouter
from fastapi_sqlalchemy import db
from app.models import User as ModelUser
from app.schema import User as SchemaUser

router = APIRouter()


@router.get("/")
async def pong():
    return {"ping": "pong!"}


@router.post("/user/", response_model=SchemaUser)
async def create_user(user: SchemaUser):
    db_user = ModelUser(
        first_name=user.first_name, last_name=user.last_name, age=user.age
    )
    db.session.add(db_user)
    db.session.commit()
    return db_user
