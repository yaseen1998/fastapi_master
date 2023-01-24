from fastapi import APIRouter, Depends, Request
# from fastapi.requests import Request
from custom_log import log
router = APIRouter(
    prefix="/dependencies",
    tags=["dependencies"],
    dependencies=[Depends(log)]
)
def conver_params(request:Request,separator:str=":"):
    out_params =[]
    for key,value in request.query_params.items():
        out_params.append(f"{key}{separator}{value}")
        
    return out_params

def convert_headers(request:Request,separator:str=":",params=Depends(conver_params)):
    out_headers =[]
    for key,value in request.headers.items():
        out_headers.append(f"{key}{separator}{value}")
        
    return {"headers":out_headers,"params":params}





@router.get("")
def get_item(test:str,headers=Depends(convert_headers),):
    return {"headers":headers}

@router.post("/new")
def create_item(headers=Depends(convert_headers),separator:str="__"):
    return {"headers":headers}



class Account:
    def __init__(self,name:str,email:str):
        self.name = name
        self.email = email
        
@router.post("/account")
def create_account(name:str,email:str,account:Account=Depends()):
    return {"account":account.__dict__}