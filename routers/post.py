from typing import List, Optional

import oauth2
from database import SessionLocal, engine, get_db
from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, Response, status
from repo import models
from schemas import PostBase, PostCreate, PostResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/post", tags=["post"])


@router.get("", response_model=List[PostResponse])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    print(limit)
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(
    post: PostBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # with the get_current_user we are getting the user_id from the token and ensure that user authenticated before creating a post
    print(current_user)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print("New Post", new_post.title, new_post.content, new_post.published)
    return new_post


# using path parameter
@router.get("/{id}", response_model=PostResponse)
def get_post(id, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with ID: {id} not found",
        )
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with ID: {id} not found"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action.",
        )

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with ID: {id} not found",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def update_post(
    id: int,
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    print("ehhere/? ", post)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with ID: {id} not found",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action.",
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
