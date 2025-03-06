from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    files_uploaded: list[str] = Field(alias="filesUploaded")


class DeleteResponse(BaseModel):
    files_deleted: list[str] = Field(alias="filesDeleted")


class ListResponse(BaseModel):
    files: list[str]
