from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import  OAuth2PasswordRequestForm
from sqlalchemy import true
from sqlalchemy.orm import Session

from app.database import get_db
from app import oauth
from app.util import hash_password, verify_password
from .. import schema, models, oauth


router = APIRouter(
    prefix = "/auth",
    tags=['Auth']
)

@router.get("/login", response_model= schema.Token )
def authenticate_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    #find if user is existing
    userExist = db.query(models.User).filter(models.User.email  == user_credentials.username).first()
    if not userExist:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, 
        detail=f"Invalid credential")

    verify_password(user_credentials.password, userExist.password )
    
    if verify_password: 
        token =  oauth.create_access_token(data = {"id": userExist.id, "email": userExist.email}) 
        return {"access_token": token, "token_type":"bearer"}
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail=f"Invalid credential")
