from fastapi import FastAPI, APIRouter, Depends, Form, HTTPException, status, File, UploadFile
from sqlalchemy import false, true
from sqlalchemy.orm import Session

from app.database import get_db
from app.util import hash_password, verify_password, convertBytesToString
from .. import schema, models, oauth


router = APIRouter(
    prefix = "/books",
    tags=['Books']
)


@router.get("/", response_model= schema.BookOut )
def get_all_book(db:Session = Depends(get_db), currentuser: int = Depends(oauth.get_current_user)):    
    book =  db.query(models.Book).one_or_none()
    return book

@router.get("/{id}", response_model= schema.BookOut )
def get_book_by_id(id: int, db:Session = Depends(get_db), currentuser: int = Depends(oauth.get_current_user)):    
    book_query =  db.query(models.Book).filter( models.Book.id ==  id )
    book = book_query.first()
    print(book_query)    
    return book

@router.post("/", response_model = schema.BookOut )
def create_book(book: schema.BookCreate, db:Session = Depends(get_db),   
    currentuser: int = Depends(oauth.get_current_user) ):

    bookExist_query = db.query(models.Book).filter(models.Book.title == book.title, models.Book.ISBN == book.ISBN)
    bookExist = bookExist_query.first()
    
    if bookExist:
        raise HTTPException(status = status.HTTP_409_CONFLICT, detail= f"Book already exist")
    
    new_book =  models.Book( createdby_id = currentuser.id , **book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.put("/{id}")
def update_book(book_updates: schema.BookOut, currentuser: int = Depends(oauth.get_current_user),
    db: Session= Depends(get_db)):
    #bookExist
    bookExist_query = db.query(models.Book).filter(models.Book.id == id)
    book_found = db.query(models.Book).filter(models.Book.id == id).first()

    if not bookExist_query:
        raise HTTPException(status = status.HTTP_404_NOT_FOUND, details = f"Book not found")
    
    if book_found.createdby_id != currentuser.id:
        raise HTTPException( status = status.HTTP_401_UNAUTHORIZED, detail= f"you are not authorized to update this book" )

    bookExist_query.update(book_updates.dict(), synchronize_session= False)
    db.commit()
    db.refresh(book_found)


@router.delete("/{id}")
def delete_book( currentuser: int = Depends(oauth.get_current_user),
    db: Session= Depends(get_db)):
    #bookExist
    bookExist_query = db.query(models.Book).filter(models.Book.id == id)
    book_found = db.query(models.Book).filter(models.Book.id == id).first()

    if not book_found:
        raise HTTPException(status = status.HTTP_404_NOT_FOUND, details = f"Book not found")
    
    if book_found.createdby_id != currentuser.id:
        raise HTTPException( status = status.HTTP_403_FORBIDDEN , detail= f"you are not authorized to delete this book" )

    bookExist_query.delete(synchronize_session= False)
    db.commit()
    db.refresh(book_found)


#bulk upload in excel file
@router.post("/bulk_upload/")
async def bulk_book_upload( file: UploadFile=File(...), db: Session= Depends(get_db),
    currentuser: int = Depends(oauth.get_current_user) ):
    contents = await file.read()
    books_to_json_string = convertBytesToString(contents)
    for book in books_to_json_string:
    #     print(book)
    #for each json excel, insert into db
        bookExist_query = db.query(models.Book).filter(models.Book.title == book.title, models.Book.ISBN == book.ISBN)
        bookExist = bookExist_query.first()
        
        if bookExist:
            raise HTTPException(status = status.HTTP_409_CONFLICT, detail= f"{book.title} already exist")
        
        new_book =  models.Book( createdby_id = currentuser.id , **book.dict())
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    #pass
    return {"file_contents": books_to_json_string}
