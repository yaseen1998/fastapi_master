from fastapi import APIRouter, Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    print(token)
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user

@router.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user