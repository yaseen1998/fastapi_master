from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str | None = None
    
class ItemCreate(ItemBase):
    pass

class ItemRelation(ItemBase):
    id: int
    owner_id: int
    
    class Config:
        orm_mode = True
        
        
class UserBase(BaseModel):
    email: str
    
class UserCreate(UserBase):
    password: str
    
class UserRelation(UserBase):
    id: int
    is_active: bool
    items_user: list[ItemRelation] = []
    
    class Config:
        orm_mode = True