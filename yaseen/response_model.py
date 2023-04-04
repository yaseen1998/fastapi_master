from typing import Any
from fastapi import APIRouter,Response
from pydantic import BaseModel, EmailStr
from fastapi.responses import JSONResponse, RedirectResponse


router = APIRouter(
    prefix="/response",
    tags = ['response']
)


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []
    email:EmailStr | None = None


@router.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@router.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]
    
@router.get("/items2/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
    
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str


@router.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user


@router.get("/portal",response_model=None)
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}
    # return JSONResponse(content={"message": "Here's your interdimensional portal."}) # without response_model=None and  | dict
    
    
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@router.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True,response_model_include={"name", "tax"}) # response_model_exclude_unset=True not to show unset values (default value) , response_model_exclude_unset=False to show unset values
async def read_item(item_id: str):
    return items[item_id]


@router.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"name"})
async def read_item_public_data(item_id: str):
    return items[item_id]
