from fastapi import HTTPException
from db.models import DbPost
from .schemas import PostBase
from sqlalchemy.orm.session import Session
import datetime

def create(db:Session,request:PostBase):
    new_post = DbPost(
        title=request.title,
        content=request.content,
        creator=request.creator,
        timstamp=datetime.datetime.now(),
        image_url=request.image_url
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



def get_all(db:Session):
    posts = db.query(DbPost).all()
    return posts



def delete_post(db:Session,id:int):
    post = db.query(DbPost).filter(DbPost.id == id)
    if not post.first():
        raise HTTPException(status_code=404,detail=f"Post with id {id} not found")
    post.delete(synchronize_session=False)
    db.commit()
    return "Post deleted successfully"