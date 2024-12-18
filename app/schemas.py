from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# Extending Base model of pydantic (Validating The data we get from request)

#user
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr
    class Config:
        orm_mode: True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# vote
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id:int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    class Config:
        orm_mode= True

class PostRespWithVotes(PostBase):
    Post: PostResponse
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int
