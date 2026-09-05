from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.import_job import ImportJobResponse
from app.services.import_service import create_import_job
from app.tasks.import_tasks import process_import_job


router = APIRouter(
    prefix="/api/imports",
    tags=["Imports"],
)

UPLOAD_DIR = Path("uploads")    # this will create a directory named "uploads" in the root directory of the project if it does not exist already
UPLOAD_DIR.mkdir(exist_ok=True)    # this will create the directory if it does not exist already, and if it does exist, it will do nothing


@router.post(
    "/upload",
    response_model=ImportJobResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_excel(
    file: UploadFile = File(...),     
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is required",
        )

    if not file.filename.lower().endswith(".xlsx"):   #validation just to support the .xlsx file 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .xlsx files are supported",
        )

    unique_filename = f"{uuid4()}_{file.filename}"    #generate unique file name
    file_path = UPLOAD_DIR / unique_filename      # this will create a path object for the file in the uploads directory with the unique filename

    with file_path.open("wb") as buffer:   #buffer will open the file in write binary mode and it will write the contents of the uploaded file to the buffer
        buffer.write(file.file.read())    # this will read the contents of the uploaded file and write it to the buffer

    import_job = create_import_job(
        db=db,
        filename=file.filename,
    )

    process_import_job.delay(
        import_job.id,
        str(file_path),
    )

    return import_job