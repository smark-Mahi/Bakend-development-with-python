from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, databasse, models, Oauth
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db:Session = Depends(databasse.get_db), current_user: models.User = Depends(Oauth.get_current_user)):
    
    post_is_exist = db.query(models.Votes).filter(models.Votes.post_id== vote.post_id).first()

    if not post_is_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id {vote.post_id} does not exist")
                                  
    vote_query = db.query(models.Votes).filter(models.Votes.post_id== vote.post_id, models.Votes.user_id== current_user.id)
    found_vote = vote_query.first()
    if (vote.dir ==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully removed vote"}
