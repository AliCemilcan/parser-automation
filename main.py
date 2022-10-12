import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from config import Settings
from database import engine
from repo import models
from routers import auth, post, user, vote

# get a session from the database and close it when request is done
models.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello World!!!"}
