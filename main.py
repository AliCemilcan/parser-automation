import psycopg2
from config import Settings
from database import SessionLocal, engine
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor
from repo import models
from repo.models import Base
from routers import auth, post, user, vote

# get a session from the database and close it when request is done
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello World!!! This is ACC speaking"}
