from fastapi import APIRouter, Response, File, UploadFile
from minio import Minio
from database.repositories import add_song
import io
import h5py

__ROUTE_PREFIX__ = "/digestion"

router = APIRouter(prefix=__ROUTE_PREFIX__)


@router.post("/processFile")
def process_h5_file(filename: str):
    # ToDo move to a different file
    minio_client = Minio(
        "localhost:9000",  # MinIO address
        access_key="admin",
        secret_key="password",
        secure=False,  # Set to True if using HTTPS
    )
    bucket_name = "my-bucket"
    # Download the file
    response = minio_client.get_object(bucket_name, filename)
    file_data = io.BytesIO(response.data)
    file_data = h5py.File(file_data, "r")
    title = file_data["metadata"]["songs"]["title"][0].decode("utf-8")
    artist = file_data["metadata"]["songs"]["artist_name"][0].decode("utf-8")
    duration = float(file_data["analysis"]["songs"]["duration"][0])

    add_song(
        title,
        artist,
        "Rock",
        album_name="A Night at the Opera",
        duration=duration,
        play_count=100,
    )
