import utils
from database import SessionLocal, engine, get_db
from repo import models
from schemas import UserCreate, UserOut
from sqlalchemy.orm import Session

from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, Response, status

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # hash the password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} not found",
        )
    return user
