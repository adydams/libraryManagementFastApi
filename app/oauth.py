from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from . import schema, models
from .database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
from jose import JWTError, jwt

from decouple import config



#when passing the data directly
#check in .env file
SECRET_KEY_Val = config('SECRET_KEY')
ALGORITHM_Val = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES_Val = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))
# SECRET_KEY
# algorithm
# expiration_time


SECRET_KEY = SECRET_KEY_Val
ALGORITHM = ALGORITHM_Val
ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES_Val
router = APIRouter()


def  create_access_token(data: dict, expires_delta: Optional[timedelta] =  None ):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str =payload.get("id")
        email: str =payload.get("email")

        if id is None:
            raise credentials_exception
        
        token_data = schema.TokenData(id =id, email = email)
        
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme),  db:Session = Depends(get_db) ):
    credentials_exception = HTTPException( 
        status_code = status.HTTP_401_UNAUTHORIZED, 
        detail= f"could not validate credentials",
        headers= {"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user
