from itertools import product
from fastapi import FastAPI,File,UploadFile
import shutil
import pytesseract
from db import models
from db.database import engine
from router import post
from fastapi.staticfiles import StaticFiles
from redis_om import get_redis_connection,HashModel

app = FastAPI()

app.include_router(post.router)


@app.post('/ocr')
def ocr(image: UploadFile = File(...)):
    filepath = 'txtFile'
    with open(filepath, 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    return pytesseract.image_to_string(filepath,lang='eng')


models.Base.metadata.create_all(engine)

redis = get_redis_connection(
    host='********',
    port='16205', 
    password='********',
    decode_responses=True
)

class Product(HashModel):
    name:str
    price:float
    quqntity:int
    class Meta:
        database=redis
        
@app.post('/product')
def create(product:Product):
    product.save()
    return product

@app.get('/product/{pk}')
def get(pk):
    return Product.get(pk=pk)

@app.get('/products')
def get_all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk:str):
    product = Product.get(pk=pk)
    return {
        'id':pk,
        'name':product.name,
        'price':product.price,
        'quqntity':product.quqntity
    }
    
@app.delete('/product/{pk}')
def delete(pk:str):
    return Product.delete(pk=pk)
    
app.mount("/files",StaticFiles(directory="files"),name="files")