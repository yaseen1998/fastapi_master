from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import models
from db.hash import Hash
from auth import oauth2

router = APIRouter(
    tags=['auth'],
)

@router.post('/token')
def get_token(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.username==request.username).first()
    hashPwd = Hash()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid credentials")
    if not hashPwd.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Incorrect password")

    access_token = oauth2.create_access_token(data={"sub":user.username})
    return {"access_token":access_token,"token_type":"bearer",'username':user.username,'id':user.id}


