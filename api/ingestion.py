from fastapi import APIRouter, UploadFile, Depends, Response, status

from api.response_models.ingestion import DeleteResponse, ListResponse, UploadResponse
from constants import DataLakeConstants
from repositories.minio import MinioRepo

__ROUTE_PREFIX__ = "/ingestion"

router = APIRouter(prefix=__ROUTE_PREFIX__, tags=["Raw files management"])


@router.post(
    "/uploadFiles", response_model=UploadResponse, status_code=status.HTTP_201_CREATED
)
def upload_multiple_files(
    files: list[UploadFile],
    replace: bool = True,
    minio_repo=Depends(MinioRepo),
) -> UploadResponse:
    """Upload files. Since it can be controlled if a file will be replaced or not,
    this endpoint can also be used for update operations,"""
    if not replace:
        existing_files = set(minio_repo.list_files(DataLakeConstants.RAW_BUCKET))

        files = [file for file in files if file.filename not in existing_files]

    for file in files:
        minio_repo.add_file(file, DataLakeConstants.RAW_BUCKET)
    return UploadResponse(
        filesUploaded=[file.filename for file in files],
    )


@router.get("/listFiles")
def list_files(
    bucket: str = DataLakeConstants.RAW_BUCKET, minio_repo=Depends(MinioRepo)
) -> ListResponse:
    """List all files in a given bucket."""
    files = minio_repo.list_files(bucket)
    return ListResponse(files=files)


@router.get("/downloadFiles")
def download_file(
    filename: str,
    bucket: str = DataLakeConstants.RAW_BUCKET,
    minio_repo=Depends(MinioRepo),
):
    response = minio_repo.download_file(bucket, filename)
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return Response(response.data, headers=headers)


@router.delete("/deleteFiles")
def remove_files(
    filenames: list[str],
    bucket: str = DataLakeConstants.RAW_BUCKET,
    minio_repo=Depends(MinioRepo),
) -> DeleteResponse:
    for filename in filenames:
        minio_repo.remove_object(bucket, filename)
    return DeleteResponse(filesDeleted=filenames)
