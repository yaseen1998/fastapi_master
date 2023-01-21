from datetime import datetime,timedelta
from typing import Optional
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import models
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECERT_KEY = 'bca726ec6bc1bba1180716077d53cc0c54b46c721934191bfa6a050859a7c42e'
ALGORITHM = 'HS256'
EXPIRE_MINUTES = 30


def create_access_token(data:dict,expires_date:Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_date:
        expire = datetime.utcnow() + expires_date
    else:
        expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode,SECERT_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        payload = jwt.decode(token,SECERT_KEY,algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username==username).first()
    if user is None:
        raise credentials_exception
    return user