from fastapi import Depends, UploadFile
from minio import Minio


def get_minio_client():
    return Minio(
        "localhost:9000",  # MinIO address
        access_key="admin",
        secret_key="password",
        secure=False,  # Set to True if using HTTPS
    )


class MinioRepo:

    def __init__(self, minio_client=Depends(get_minio_client)):
        self.minio_client = minio_client

    def add_file(self, file: UploadFile, bucket_name: str) -> None:
        self.minio_client.put_object(bucket_name, file.filename, file.file, file.size)
        return
