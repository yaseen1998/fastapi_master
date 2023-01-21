from fastapi import APIRouter, Depends
from db.database import get_db

from db.schemas import ArticalBase, ArticalDisplay, UserBase
from sqlalchemy.orm import Session
from auth.oauth2 import oauth2_scheme,get_current_user
from db import db_artical

router = APIRouter(
    prefix="/artical",
    tags = ['artical']
)

@router.post('/create',response_model=ArticalDisplay)
def artical_create(request:ArticalBase,db:Session=Depends(get_db)):
    return db_artical.create_artical(db,request)

@router.get('/read/{id}',
            # response_model=ArticalDisplay
            )
def artical_retrive(id:int,db:Session=Depends(get_db),
                    # token:str=Depends(oauth2_scheme)
                    current_user:UserBase=Depends(get_current_user)
                    ):
    return {'data':db_artical.get_artical_by_id(db,id),'current_user':current_user}
