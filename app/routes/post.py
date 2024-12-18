from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, Oauth
from ..databasse import  get_db
from sqlalchemy.orm import Session
from typing import List
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostRespWithVotes])
def getAll_posts(db:Session = Depends(get_db), user: models.User = Depends(Oauth.get_current_user), limit: int = 5, skip:int = 0, search:Optional[str] = ""):
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/sqlalchemy")
async def root():
    return {"message": "Hello World"}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate,db:Session = Depends(get_db), user: models.User = Depends(Oauth.get_current_user)):
    print(user,"ark")
    new_Post = models.Post(owner_id=user.id, **post.model_dump())
    db.add(new_Post)
    db.commit()
    db.refresh(new_Post)
    return new_Post

@router.get("/{id}", response_model=schemas.PostRespWithVotes)
def get_post(id:int,db:Session = Depends(get_db), user:models.User = Depends(Oauth.get_current_user)):
    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db), user:models.User = Depends(Oauth.get_current_user)):
    deletedPost_query = db.query(models.Post).filter(models.Post.id==id)
    
    deletedPost=deletedPost_query.first()

    if deletedPost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    

    if deletedPost.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

     
    deletedPost_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.PostCreate,db:Session = Depends(get_db), user:models.User = Depends(Oauth.get_current_user)):
    updatedPost_query = db.query(models.Post).filter(models.Post.id==id)
    
    updatedPost=updatedPost_query.first()
    
    if updatedPost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    
    if updatedPost.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    updatedPost.update(post.model_dump(),synchronize_session=False)
    db.commit()

    return updatedPost_query.first()