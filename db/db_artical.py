
import re
from fastapi import HTTPException,status
from sqlalchemy.orm.session import Session

from db.models import Artical

from db.schemas import ArticalBase
from exception import StoryException

def create_artical(db:Session,request:ArticalBase):
        if request.content.startswith("One"):
            raise StoryException("Story can't start with One")
    
        new_artical = Artical(
    
            title=request.title,
    
            content=request.content,
    
            published=request.published,
    
            user_id= request.creator_id
    
        )
    
        db.add(new_artical)
    
        db.commit()
    
        db.refresh(new_artical)
    
        return new_artical
    
def get_artical_by_id(db:Session,id:int):
        artical = db.query(Artical).filter(Artical.id == id).first()
        if artical:
            return artical
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Artical with id {id} not found")