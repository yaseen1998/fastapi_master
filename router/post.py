import shutil
import string
from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user
from db.schemas import PostBase, PostBase2, PostDisplay2, UserBase
from db.database import get_db
from db import db_post, db_post2
import random
router = APIRouter(
    prefix="/post",
    tags=["post"],
)



@router.post('/create')
def create_post(request: PostBase, db: Session = Depends(get_db)):
    return db_post.create(db, request)



@router.get('/all')
def get_all(db: Session = Depends(get_db)):
    return db_post.get_all(db)


@router.delete('/delete/{id}')
def delete_post(id:int,db:Session = Depends(get_db)):
    return db_post.delete_post(db, id)


@router.post('/image')
def upload_image(image: UploadFile = File(...)):
    letter = string.ascii_letters
    print('letter',letter)
    rand_str = ''.join(random.choice(letter) for i in range(10))
    print('rand_str',rand_str)
    new = f"_{rand_str}."
    print('new',new)
    namefile = image.filename.split('.', 1)
    print('namefile',namefile)
    filename = new.join(namefile)
    print('filename',filename)
    path = f"files/{filename}"
    
    with open(path, 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    return {"filename": filename}


image_url_type=['absolute','relative']
@router.post('/create2',response_model=PostDisplay2)
def create_post(request: PostBase2, db: Session = Depends(get_db),current_user:UserBase=Depends(get_current_user)):
    if request.image_url_type not in image_url_type:
        raise HTTPException(status_code=400,detail="image_url_type must be absolute or relative")
    return db_post2.create(db, request)

@router.get('/all2',response_model=List[PostDisplay2])
def get_all(db: Session = Depends(get_db)):
    return db_post2.get_all(db)


@router.delete('/delete2/{id}')
def delete_post(id:int,db:Session = Depends(get_db),current_user:UserBase=Depends(get_current_user)):
    return db_post2.delete_post(db, id,current_user.id)