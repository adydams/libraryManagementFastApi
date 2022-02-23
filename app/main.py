from operator import ge
from typing import Optional
from fastapi import FastAPI, File, UploadFile
from .routers import user, book, auth, blob,payscribe, geolocations
from fastapi.responses import HTMLResponse
from urllib.request import urlopen

app = FastAPI()

app.include_router(book.router)
app.include_router(user.router)
app.include_router(auth.router)
#app.include_router(blob.router)
app.include_router(payscribe.router)
app.include_router(geolocations.router)


@app.get("/")
def read_root():
  return {"Hello": "World"}
    

@app.get("/items/{item_id}") 
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/files/")
async def create_files(files: list[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.get("/")
def upload_files():
    content = """
    <body>
    <form action="/files/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    </body>
        """
    return HTMLResponse(content=content)


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}



