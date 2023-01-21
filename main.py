from fastapi import FastAPI, HTTPException, Request,responses,status
from exception import StoryException
from router import blog_get,blog_post,user,artical,product
from db import models
from db.database import engine
from auth import authintaction
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.include_router(user.router)
app.include_router(artical.router)
app.include_router(product.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(authintaction.router)

@app.get('/')
def index():
    return {"message":'hello world'}

    

@app.exception_handler(StoryException)
def story_exception_handler(request:Request,exc:StoryException):
    return responses.JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message":f"{exc.msg}"}
    )


# @app.exception_handler(HTTPException)
# def custom_handler(request:Request,exc:HTTPException):
#     return responses.PlainTextResponse(
#         status_code=exc.status_code,
#         content=f"{exc.detail}"
#     )
    
models.Base.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)