from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
router = APIRouter(
    prefix="/file",
    tags=['file']
)

@router.post('/upload')
def get_file(file:bytes=File(...)):
    # must by txt file
    content = file.decode('utf-8')
    lines = content.splitlines()

    return {'file_size':lines}


@router.post('/upload2')
def upload_file(file:UploadFile=File(...)):
    path = f"files/{file.filename}"
    with open(path,'wb') as f:
        f.write(file.file.read())
    return {'filename':file.filename,'type':file.content_type}


@router.get('/download/{filename}',response_class=FileResponse)
def download_file(filename:str):
    path = f"files/{filename}"
    print('path: ',path)
    return path