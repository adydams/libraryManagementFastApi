from pydantic import BaseModel
from pydantic.types import conint
from typing import Optional
from datetime import datetime

from pydantic.networks import EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserLogin):
   phone_number: Optional[str]
   
    
class BookCreate(BaseModel):
    title: str
    author: str
    published: bool = False
    ISBN: Optional[str]

class BookReview(BaseModel):
    book_id: int
    review: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class BookOut(BookCreate):
    id: Optional[int]
    title: Optional[str]
    published: Optional[str]
    author: Optional[str]
    createdby_id : Optional[int]
    createdby: UserOut
   
    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
        
    class Config:
        orm_mode = True

class DataLookUp(BaseModel):
    network: str

class DataVend(BaseModel):
    plan: str
    recipent: str
    network: str
