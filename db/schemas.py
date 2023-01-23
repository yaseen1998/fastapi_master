from typing import List
from pydantic import BaseModel


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


