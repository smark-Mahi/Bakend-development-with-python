from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas, databasse, models, utils, Oauth
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router= APIRouter(
    tags=["Authentication"]
)

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(databasse.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #create token
    access_token = Oauth.create_access_token(data= {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}