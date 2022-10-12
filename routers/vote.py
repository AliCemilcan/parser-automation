# from .. import database, models, oauth2, schemas
import oauth2
from database import SessionLocal, engine, get_db
from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, Response, status
from repo import models
from schemas import Vote
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    vote_found = vote_query.first()
    if vote.dir == 1:
        if vote_found:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.email} has already voted on post",
            )

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully voted on post"}
    else:
        if not vote_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote doesnot exists "
            )
        # we have a vote, lets delete the vote
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}
