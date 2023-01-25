from fastapi import FastAPI,File,UploadFile
import shutil
import pytesseract
from db import models
from db.database import engine
from router import post
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(post.router)


@app.post('/ocr')
def ocr(image: UploadFile = File(...)):
    filepath = 'txtFile'
    with open(filepath, 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    return pytesseract.image_to_string(filepath,lang='eng')


models.Base.metadata.create_all(engine)

app.mount("/files",StaticFiles(directory="files"),name="files")