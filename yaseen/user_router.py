from fastapi import APIRouter, Depends, HTTPException
from yaseen.database import get_db

from yaseen.user_base import ItemCreate, ItemRelation, UserCreate, UserRelation
from sqlalchemy.orm import Session

from yaseen.user_datebase import Item, User

router = APIRouter(
    prefix="/user",
    tags = ['user']
)
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def get_items_for_user(db: Session, user_id: int):
    return db.query(Item).filter(Item.owner_id == user_id).all()

def create_user_item(db: Session, item: ItemCreate, user_id: int):
    db_item = Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



@router.post('/create',response_model=UserRelation)
async def create_user_router(user:UserCreate,db:Session=Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)
        

@router.get('/get_all',response_model=list[UserRelation])
async def get_users_router(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

# get one user
@router.get('/get_one/{user_id}',response_model=UserRelation)
async def get_user_router(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# create Item for user
@router.post('/create_item/{user_id}',response_model=ItemRelation)
async def create_item_router(user_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    return create_user_item(db=db, item=item, user_id=user_id)


@router.get('/get_all_items',response_model=list[ItemRelation])
async def get_items_router(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_items(db, skip=skip, limit=limit)
    return items

@router.get('/get_all_items/{user_id}',response_model=list[ItemRelation])
async def get_items_for_user_router(user_id: int, db: Session = Depends(get_db)):
    items = get_items_for_user(db, user_id=user_id)
    return items