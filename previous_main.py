from fastapi import Depends, FastAPI, HTTPException, Header,Query,Path,Body,Cookie, Request,status
from typing import Union, Optional
from pydantic import BaseModel,Field,HttpUrl,Required
from enum import Enum
from datetime import datetime, time, timedelta
from uuid import UUID
from yaseen import response_model,extra_models,request_file,Dependency,auth,user_router
from yaseen.handle_error import UnicornException
from fastapi.responses import JSONResponse,PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import time as ti
from yaseen.database import  engine
from yaseen import user_datebase
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
async def global_verify_token(company: str = Header()):
    if company != "yasen":
        raise HTTPException(status_code=400, detail="company header invalid")
    
user_datebase.Base.metadata.create_all(bind=engine)

app = FastAPI(dependencies=[Depends(global_verify_token)])
app.include_router(response_model.router)
app.include_router(extra_models.router)
app.include_router(request_file.router)
app.include_router(Dependency.router)
app.include_router(auth.router)
app.include_router(user_router.router)

class Image(BaseModel):
    url: str
    name: str
    hturl :HttpUrl
    
class Item(BaseModel):
    description: Union[str, None] = None
    price: float=Field(gt=0, description="The price must be greater than zero",example=36)
    tax: Optional[float] = None
    name: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    tags : list[str] | None = None
    tagset : set[str] | None = None
    image: Image | None = None
    images : list[Image] | None = None
    
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/union/{id}")
def read_item(id: int, q: Union[str, None] = None):
    return {"id": id, "q": q}


@app.put("/union/{id}")
def update_item(id: int, item: Item|None = None):
    return {"id": id, "item": item}


@app.get("/enum/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/items")
async def read_items(needy: str,q: Optional[str] = None,param: str | None = None,short: bool = False,):
    return {"q": q, "param": param, "short": short, "needy": needy}

@app.post("/items") 
def create_items(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.get("/itemsQuery")
async def read_query_items( q: str | None = Query(default='mick', max_length=5,deprecated=True,),
                            hidden: str | None = Query(default=None, include_in_schema=False),
                            params: str | None = Query(default=None, max_length=50, regex="^fixedquery$"),
                            qy: str | None = Query(default=..., max_length=50),
                            qy2: str | None = Query(default=Required, max_length=50),
                            lis: list[str]|None = Query(default=["foo", "bar"],alias="item-query"),
                            ti: str | None = Query(default=None, title="Query string", description="Query string for the items to search in the database that have a good match", min_length=3)
                            ):

    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q, "params": params, "qy": qy, "qy2": qy2, "lis": lis, "ti": ti, "hidden": hidden})
    return results


@app.get("/itemsPath/{item_id}")
async def read_path_items(item_id: int = Path(title="The ID of the item to get", ge=1, le=1000, description="The ID of the item to get", alias="item-id")):
    return {"item_id": item_id}


@app.put("/itemsBody")
async def update_item(weights: dict[int, float], 
                      images: list[Image] | None = Body(default=None, embed=True,
                                                        example=[{"url": "http://example.com/baz.jpg", "name": "The Foo live",'hturl':'http://example.com/baz.jpg'}] # works if images alone
                                                        ),
                      importance: int = Body(gt=0), 
                      
                      item: Item = Body(embed=False)): # item:{ "name": "Foo", "description": "The pretenders", "price": 42.0, "tax": 3.2} with embed=True and { "name": "Foo", "description": "The pretenders", "price": 42.0, "tax": 3.2} with embed=False
    results = { "importance": importance, "item": item, "images": images, "weights": weights}
    return results

@app.put("/itemsBody2")
async def update_item2(
    *,
    item_id: int,
    item: Item = Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "zoobar",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/itemField")
async def itemField(
    item_id: UUID,
    start_datetime: datetime | None = Body(default=None),
    end_datetime: datetime | None = Body(default=None),
    repeat_at: time | None = Body(default=None),
    process_after: timedelta | None = Body(default=None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }
    
@app.get("/cookies")
async def read_cookies(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}


@app.get("/headers")
async def header(user_agent: str | None = Header(default=None),x_token: list[str] | None = Header(default=None)):
    return {"User-Agent": user_agent, "X-Token values": x_token}


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


# @app.exception_handler(StarletteHTTPException) # override default exception handler
# async def http_exception_handler(request, exc):
#     print(f"HTTPException: {exc.detail} ({exc.status_code})")
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# @app.exception_handler(RequestValidationError) # override default exception handler for validation errors
# async def validation_exception_handler(request, exc):
#     print(f"RequestValidationError: {exc}")
#     # return PlainTextResponse(str(exc), status_code=400)
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
#     )

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = ti.time()
    print("start_time",start_time)
    response = await call_next(request)
    process_time = ti.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)