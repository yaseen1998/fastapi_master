from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from templates.schemas import ProductBase
router = APIRouter(
    prefix="/templates",
    tags=['templates']
)

templates = Jinja2Templates(directory="templates")

@router.post("product/{id}",response_class=HTMLResponse)
def get_product(id:str,product:ProductBase,
                request:Request):
    print('product',product)
    return templates.TemplateResponse("product.html",{"request":request,"id":id,
                                                      'product':product,
                                                      })