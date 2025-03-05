from fastapi import APIRouter, UploadFile, Depends

from repositories.minio import MinioRepo

__ROUTE_PREFIX__ = "/ingestion"

router = APIRouter(prefix=__ROUTE_PREFIX__)


@router.post("/uploadFile")
def upload_h5_file(file: UploadFile, minio_repo=Depends(MinioRepo)):
    minio_repo.add_file(file, "raw")

    return {"filename": file.filename}


@router.post("/uploadFiles")
def upload_multiple_h5_file(files: list[UploadFile], minio_repo=Depends(MinioRepo)):
    for file in files:
        minio_repo.add_file(file, "raw")

    return {"filenames": [file.filename for file in files]}
