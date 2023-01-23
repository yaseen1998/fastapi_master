from enum import Enum
from typing import Optional
from fastapi import APIRouter, Depends, Response,status
from custom_log import log

from router.blog_post import required_functionality

router = APIRouter(
    prefix = '/blog',
    tags=['blog']
    
)

@router.get('/all',
         status_code=status.HTTP_200_OK,
         summary="retrive all bloc",
         description="call all bloc data"
         )
def bloc_all():
    return {'message:"all bl'}
# order is import all is string but id is int 
@router.get('/{id}',tags=['id'])
def bloc(id:int,response:Response):
    log(tag="bloc",message=f"retrive bloc {id}")
    if id>5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error":f"bloc {id}"}
    response.status_code = status.HTTP_200_OK
    return {'message':f'this is your {id}'}


class BlogType(str,Enum ):
    short="short"
    story="story"
    howto="howto"
    
 
def bloc_type(type:BlogType):
    """
    - retrive data type
    - **use** Enum to get data as select
    """
    return {"message":f"blog type {type}"}


@router.get("/param")
def bloc_param(page=10,size:Optional[int]=None,param:dict=Depends(required_functionality)):
    return {"message":f"all {page} size {size}","res":param }

@router.get('/query/{id}')
def query_bloc(id:int,valid:bool=True,username:Optional[str]=None):
    return {"message":f"hello {id} valid {valid} username {username}"}