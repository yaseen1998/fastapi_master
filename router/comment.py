from fastapi import APIRouter, Depends, Response,status
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user
from db.schemas import CommanBase
from db.database import get_db
from db import db_comment

router = APIRouter(
    prefix = '/comment',
    tags=['comment']
    
)

@router.post('/create')
def create(request:CommanBase,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return db_comment.create_comment(db, request)


@router.get('/all/{post_id}')
def get_all_comments(post_id:int,db:Session=Depends(get_db)):
    return db_comment.get_all(db, post_id)