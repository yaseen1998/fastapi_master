from fastapi import HTTPException
from db.models import DbPost2
from .schemas import PostBase2
from sqlalchemy.orm.session import Session
import datetime

def create(db:Session,request:PostBase2):
    new_post = DbPost2(
        title=request.title,
        timestamp=datetime.datetime.now(),
        image_url=request.image_url,
        image_url_type=request.image_url_type,
        caption = request.caption,
        user_id=request.creator_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



def get_all(db:Session):
    posts = db.query(DbPost2).all()
    return posts



def delete_post(db:Session,id:int,user_id:int):
    post = db.query(DbPost2).filter(DbPost2.id == id).first()
    if post:
        raise HTTPException(status_code=404,detail=f"Post with id {id} not found")
    if post.user_id != user_id:
        raise HTTPException(status_code=403,detail="You are not allowed to delete this post")
    db.delete(post)
    db.commit() 
    return "Post deleted successfully"