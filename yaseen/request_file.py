from fastapi import APIRouter,File, Form, UploadFile
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/request_file",
    tags=["request_file"],
)

@router.post("/files/")
async def create_files(
    files: list[bytes] = File(description="Multiple files as bytes"),
):
    print(files)
    return {"file_sizes": [len(file) for file in files]}


@router.post("/uploadfiles/")
async def create_upload_files(
    files: list[UploadFile]|None = File(description="Multiple files as UploadFile",default=None),
):
    print(files)
    return {"filenames": [file.filename for file in files]}


@router.get("/html/")
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


@router.post("/files_form/")
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }