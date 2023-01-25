from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from db.hash import Hash
from db.models import User

from db.schemas import UserBase

def create_user(db:Session,request:UserBase):
    hashPwd = Hash()
    new_user = User(
        username=request.username,
        email=request.email,
        password=hashPwd.bcrypt(request.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db:Session):
    return db.query(User).all()


def get_user_by_id(db:Session,id:int):
    return db.query(User).get(id)

def get_user_by_username(db:Session,username:str):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        raise HTTPException(status_code=404,detail=f"User with username {username} not found")
    return user

def  update_user(db:Session,id:int,request:UserBase):
    hashPwd = Hash()
    user = db.query(User).filter(User.id==id)
    user.update(
        {
        User.username:request.username,
         User.email:request.email,
         User.password:hashPwd.bcrypt(request.password)
         }
    )
    db.commit()
    return 'user updated'

def delete_user(db:Session,id:int):
    user = db.query(User).get(id)
    db.delete(user)
    db.commit()
    return 'user deleted'