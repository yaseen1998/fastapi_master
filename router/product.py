from fastapi import APIRouter
from fastapi.responses import Response,HTMLResponse,PlainTextResponse



router = APIRouter(
    prefix="/product",
    tags = ['product']
)

product = ['watch','camera','laptop','mobile']

@router.get('/read')
def get_al_product():
    data = " ".join(product)
    return Response(content=data,status_code=200,media_type='text/plain')


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