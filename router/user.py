from typing import List
from fastapi import APIRouter, Depends
from db.database import get_db

from db.schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session

from db import db_user

router = APIRouter(
    prefix="/user",
    tags = ['user']
)

@router.post('/create',response_model=UserDisplay)
def create_user(request:UserBase,db:Session=Depends(get_db)):
    return db_user.create_user(db,request)

@router.get('/read',response_model=List[UserDisplay])
def read_user(db:Session=Depends(get_db)):
    return db_user.get_all_users(db)


@router.get('/read/{id}',response_model=UserDisplay)
def retrive_user(id:int,db:Session=Depends(get_db)):
    return db_user.get_user_by_id(db,id)

@router.put('/update/{id}')
def update(id:int,request:UserBase,db:Session=Depends(get_db)):
    return db_user.update_user(db,id,request)


@router.delete('/delete/{id}')
def deleteUser(id:int,db:Session=Depends(get_db)):
    return db_user.delete_user(db,id)