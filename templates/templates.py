from fastapi import APIRouter, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from custom_log import log
from templates.schemas import ProductBase
import time
router = APIRouter(
    prefix="/templates",
    tags=['templates']
)

templates = Jinja2Templates(directory="templates")

@router.post("product/{id}",response_class=HTMLResponse)
def get_product(id:str,product:ProductBase,
                request:Request,
                bt:BackgroundTasks
                ):
    bt.add_task(log_template_call,f'template called {id}')
    return templates.TemplateResponse("product.html",{"request":request,"id":id,
                                                      'product':product,
                                                      })
    
    
    
def log_template_call(message:str):
    time.sleep(10)
    log('info',message)