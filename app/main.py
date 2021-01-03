import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from . import models
from .api import user, post, comment
from .database import engine

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users",
    },
    {
        "name": "posts",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(
    title="Blog API",
    description="Learning fastapi",
    openapi_tags=tags_metadata,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(os.path.abspath(os.path.join(BASE_DIR, os.pardir)), ".env"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


app.include_router(user.router, tags=['users'])
app.include_router(post.router, tags=['posts'])
app.include_router(comment.router, tags=['comments'])
