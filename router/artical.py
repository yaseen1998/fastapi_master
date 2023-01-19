from fastapi import APIRouter, Depends
from db.database import get_db

from db.schemas import ArticalBase, ArticalDisplay
from sqlalchemy.orm import Session

from db import db_artical

router = APIRouter(
    prefix="/artical",
    tags = ['artical']
)

@router.post('/create',response_model=ArticalDisplay)
def artical_create(request:ArticalBase,db:Session=Depends(get_db)):
    return db_artical.create_artical(db,request)

@router.get('/read/{id}',response_model=ArticalDisplay)
def artical_retrive(id:int,db:Session=Depends(get_db)):
    return db_artical.get_artical_by_id(db,id)
