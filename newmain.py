from fastapi import FastAPI,File,UploadFile
import shutil
import pytesseract

app = FastAPI()

@app.post('/ocr')
def ocr(image: UploadFile = File(...)):
    filepath = 'txtFile'
    with open(filepath, 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    return pytesseract.image_to_string(filepath,lang='eng')