from http.client import HTTPResponse
from fastapi import Depends, UploadFile
from minio.commonconfig import CopySource

from database.connection import get_minio_client


class MinioRepo:

    def __init__(self, minio_client=Depends(get_minio_client)):
        self.minio_client = minio_client

    def add_file(self, file: UploadFile, bucket_name: str) -> None:
        self.minio_client.put_object(bucket_name, file.filename, file.file, file.size)
        return

    def list_files(self, bucket: str) -> list[str]:
        return [f.object_name for f in self.minio_client.list_objects(bucket)]

    def download_file(self, bucket: str, filename: str) -> HTTPResponse:
        return self.minio_client.get_object(bucket, filename)

    def move_file(
        self, filename: str, source_bucket: str, destination_bucket: str
    ) -> None:
        cs = CopySource(source_bucket, filename)
        # Copy the object to the destination bucket
        self.minio_client.copy_object(destination_bucket, filename, cs)

        # Remove the object from the source bucket
        self.remove_object(source_bucket, filename)
        return

    def remove_object(self, bucket: str, filename: str):
        self.minio_client.remove_object(bucket, filename)
        return
