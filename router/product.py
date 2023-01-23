from typing import List, Optional
from fastapi import APIRouter, Cookie, Form, Header
from fastapi.responses import Response,HTMLResponse,PlainTextResponse
import time


router = APIRouter(
    prefix="/product",
    tags = ['product']
)

product = ['watch','camera','laptop','mobile']

@router.get('/read')
def get_al_product(response:Response,
    custom_header:Optional[str]=Header(None),
                   head:Optional[List[str]]=Header(None)
                   ):
    if head:
        response.headers['x-custom-header'] = ", ".join(head)
    
    data = " ".join(product)
    return Response(content=data,status_code=200,media_type='text/plain')

async def timeConsumingFunction():
    time.sleep(5)

@router.get('/cookie')
async def get_cookie(custom_cookie:Optional[str]=Cookie(None)):
    await timeConsumingFunction()
    if custom_cookie:
        return {'message':f'your cookie is {custom_cookie}'}
    response = Response(content='hello',status_code=200,media_type='text/plain')
    response.set_cookie(key='custom_cookie',value='hello')
    
    return {'message':'hello'}


@router.post('/form')
def create_form(name:str=Form(...)):
    return {'message':f'hello {name}'} 

@router.get("{id}",responses={
    200:{"model":str,
         'content':{ "text/html": {"example": "<div><h1>product</h1></div>" }, },
         "description":"Return product name",
         },
    400:{"model":str,
         "description":"Return error message",
         "content":{ "text/plain": { "example":"Plese enter id between 0 to 3" }, },
         }
    })
def get_product(id:int):
    if id > len(product):
        out = f"Plese enter id between 0 to {len(product)-1}"
        return Response(content=out,status_code=400,media_type='text/plain')
    products = product[id]
    out = f"""
    <head>
    <style>
    .product {{
        width: 100px;
        height: 100px;
        border: 1px solid black;
        background-color: #f1f1f1;
        text-align: center;
        }}
        </style>
        </head>
        <div class="product">
        <h1>{products}</h1>
        </div>
    
    """
    return HTMLResponse(content=out,status_code=200,media_type='text/html')