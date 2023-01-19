from typing import Dict, List, Optional
from fastapi import APIRouter, Body, Path, Query
from pydantic import BaseModel

router = APIRouter(
    prefix="/blog",
    tags = ['blog']
)

class Image(BaseModel):
    url:str
    alias:str
    
class BlogModel(BaseModel):
    titil:str
    content:str
    publised:Optional[bool]
    nb_comment:int
    tags:List[str]= []
    metadate:Dict[str,str] = {"key":"value"}
    image:Optional[Image]=None
    


@router.post('/new/{id}')
def create_blog(blog:BlogModel,id:int,version:int=1):
    return {'data':blog,'id':id,'version':version}

@router.post("/new/{id}/comment")
def create_comment(blog:BlogModel,
                   id:int=Path(None,ge=5,le=10),
                   comment_id:int=Query(None,
                                        title='id of the comment',
                                        description='some description for comment id',
                                        alias='commentId',
                                        deprecated=True
                                        ),
                   content:str=Body('how are you'),
                   content2:str=Body(...,
                                     min_length=10,
                                     max_length=20,
                                     regex="^[a-z\s]*$" # lower case and space
                                     ),# Ellipsis another option
                   v:Optional[List[str]]=Query(['1','2','3']) # or you can use None
                   ):
    return {'body':blog,'id':id,'comment':comment_id,'content':content,'content2':content2,'version':v}


def required_functionality():
    return {'message':'learning fastapi'}