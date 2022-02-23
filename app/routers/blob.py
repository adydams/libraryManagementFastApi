from fastapi import FastAPI, APIRouter
from fastapi import FastAPI, APIRouter, Depends, Form, File, UploadFile
from sqlalchemy import false, true
from sqlalchemy.orm import Session
from ..azure_blob_functions.blob import delete_blob, download_blob, get_blob, upload_blob
from azure.storage.blob import  __version__
from app.database import get_db

router = APIRouter(    
    tags=['Uploads'],
    prefix = "/uploads"
  
)


@router.post("/upload")
async def upload( container: str = Form(...), file: UploadFile=File(...), db: Session= Depends(get_db)
    #, currentuser: int = Depends(oauth.get_current_user)
     ):

    try:
        print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")
        data = await file.read()
        filename= file.filename
        return upload_blob(filename, container, data)

    except Exception as ex:
        print('Exception:')
        print(ex)


@router.get("/file/{container}/{filename}")
def get_file(container: str , filename: str ):
   return get_blob(filename, container)



@router.get("/download/{container}/{filename}")
def download_file(container: str, filename: str):
   return download_file(filename, container)

@router.delete("/delete")
def delete_file(container: str , filename: str ):
   return delete_blob(filename, container)



