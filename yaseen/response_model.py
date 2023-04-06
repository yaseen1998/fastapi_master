from typing import Any
from fastapi import APIRouter,Response
from pydantic import BaseModel, EmailStr
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from yaseen.handle_error import UnicornException


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

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@router.post("/items/")
async def create_item(item: Item) -> Item:
    return item

@router.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True) # exclude_unset=True will exclude the fields that are not set in the request body
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item

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
    
    



@router.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True,response_model_include={"name", "tax"}) # response_model_exclude_unset=True not to show unset values (default value) , response_model_exclude_unset=False to show unset values
async def read_item(item_id: str):
    if item_id not in items:
        raise UnicornException(name=item_id)
    return {"item": items[item_id]}


@router.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"name"})
async def read_item_public_data(item_id: str):
    return items[item_id]
