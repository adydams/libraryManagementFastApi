from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlalchemy import true
from sqlalchemy.orm import Session

from app.database import get_db
from app.util import hash_password, verify_password
from .. import schema, models


router = APIRouter(
     prefix = "/user",
    tags=['Users']
)

@router.post("/user/create", response_model= schema.UserOut )
def create_user(user: schema.UserCreate, db:Session = Depends(get_db)):
    
    user.password =  hash_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

