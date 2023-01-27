from fastapi import FastAPI, HTTPException, Request,responses,status
from exception import StoryException
from router import blog_get,blog_post,user,artical,product,file,dependencies,post,comment
from db import models
from db.database import engine
from auth import authintaction
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from templates import templates
import time
from fastapi.responses import HTMLResponse
from client import html
from fastapi.websockets import WebSocket


app = FastAPI()
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(artical.router)
app.include_router(product.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(authintaction.router)
app.include_router(file.router)
app.include_router(templates.router)
app.include_router(dependencies.router) 

@app.get('/')
def index():
    return {"message":'hello world'}


    

@app.exception_handler(StoryException)
def story_exception_handler(request:Request,exc:StoryException):
    return responses.JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message":f"{exc.msg}"}
    )
    
@app.get("/socket")
async def get_exception():
    return HTMLResponse(html)

clients = []
@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(f"Message text was: {data}")


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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    response.headers["duration"] = str(time.time() - start_time)
    return response
app.mount("/files",StaticFiles(directory="files"),name="files")
app.mount("/templates/static",StaticFiles(directory="templates/static"),name="static")