from fastapi import APIRouter, Response, File, UploadFile
from minio import Minio

__ROUTE_PREFIX__ = "/ingestion"

router = APIRouter(prefix=__ROUTE_PREFIX__)


@router.post("/uploadFile")
def upload_h5_file(file: UploadFile):
    minio_client = Minio(
        "localhost:9000",  # MinIO address
        access_key="admin",
        secret_key="password",
        secure=False,  # Set to True if using HTTPS
    )
    bucket_name = "my-bucket"
    minio_client.put_object(bucket_name, file.filename, file.file, file.size)

    return {"filename": file.filename}
