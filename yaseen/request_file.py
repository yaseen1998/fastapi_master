from datetime import datetime 
from fastapi import APIRouter,File, Form, UploadFile,status
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
router = APIRouter(
    prefix="/request_file",
    tags=["request_file"],
)

@router.post("/files/",status_code=status.HTTP_201_CREATED,tags=["request_file2"])
async def create_files(
    files: list[bytes] = File(description="Multiple files as bytes"),
):
    print(files)
    return {"file_sizes": [len(file) for file in files]}


@router.post("/uploadfiles/",summary="summary uploadfiles",description="description uploadfiles")
async def create_upload_files(
    files: list[UploadFile]|None = File(description="Multiple files as UploadFile",default=None),
):
    print(files)
    return {"filenames": [file.filename for file in files]}


@router.get("/html/",deprecated=True)
async def main():
    content = """
<body>
<form action="/request_file/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/request_file/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


@router.post("/files_form/", response_description="response_description The created item")
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
    
    
@router.post("/date_time/")
async def create_date_time(date:datetime):
    encode_date = jsonable_encoder(date)
    return {"date":encode_date}