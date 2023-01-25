from typing import List
from pydantic import BaseModel
import datetime

class ArticalUser(BaseModel):
    title:str
    content:str
    published:bool
    class Config():
        orm_mode=True

class UserBase(BaseModel):
    username:str
    email:str
    password:str
    
    
class UserDisplay(BaseModel):
    username:str
    email:str
    items:List[ArticalUser] = []
    class Config():
        orm_mode=True
        
        
class ArticalBase(BaseModel):
    title:str
    content:str
    published:bool
    creator_id:int
    
class UserArtical(BaseModel):
    username:str
    id:int
    class Config():
        orm_mode=True

      

class ArticalDisplay(BaseModel):
    title:str
    content:str
    published:bool
    user:UserArtical
    class Config():
        orm_mode=True



class PostBase(BaseModel):
    title:str
    content:str
    creator:str
    image_url:str
    

class PostDisplay(BaseModel):
    id:int
    title:str
    content:str
    creator:str
    image_url:str
    timstamp:datetime.datetime
    class Config():
        orm_mode=True


class PostBase2(BaseModel):
    image_url:str
    image_url_type:str
    caption:str
    creator_id:int
    title:str

class Comment(BaseModel):
    username:str
    text:str
    post_id:int
    timestamp:datetime.datetime
    class Config():
        orm_mode=True
        
class PostDisplay2(BaseModel):
    id:int
    image_url:str
    image_url_type:str
    caption:str
    timestamp:datetime.datetime
    user:UserArtical
    comments:List[Comment] = [] 
    class Config():
        orm_mode=True
        


class CommanBase(BaseModel):
    username:str
    text:str
    post_id:int