from fastapi import HTTPException
from db.models import DbComment
from .schemas import CommanBase
from sqlalchemy.orm.session import Session
import datetime

def create_comment(db:Session, request:CommanBase):
    new_comment = DbComment(username=request.username,text=request.text,post_id=request.post_id,timestamp=datetime.datetime.now())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_all(db:Session,post_id:int):
    return db.query(DbComment).filter(DbComment.post_id==post_id).all()