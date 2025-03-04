import io
from typing import Optional
from fastapi import Depends
import h5py
import requests

from repositories.minio import MinioRepo
from repositories.postgre import LyricsRepo, SongsRepo


class DigestionController:
    def __init__(
        self,
        minio_repo=Depends(MinioRepo),
        songs_repo=Depends(SongsRepo),
        lyrics_repo=Depends(LyricsRepo),
    ):
        self._minio_repo = minio_repo
        self._songs_repo = songs_repo
        self._lyrics_repo = lyrics_repo

    def process_h5_files_in_bucket(self):
        source_bucket = "my-bucket"
        destination_bucket = "processed"
        processed_songs = []
        for file in self._minio_repo.list_files():
            response = self._minio_repo.download_file(source_bucket, file.object_name)
            file_data = io.BytesIO(response.data)
            processed_songs.append(self._h5_to_dict(file_data))
            self._minio_repo.move_files(
                file.object_name, source_bucket, destination_bucket
            )
        self.songs_repo.add_songs_with_features(processed_songs)

    def add_lyrics(self):
        songs_without_lyrics = self._songs_repo.get_songs_without_lyrics()
        new_lyrics = [
            {
                "title": song.title,
                "lyrics": self._request_lyrics(song.artist_name, song.title),
            }
            for song in songs_without_lyrics
        ]
        self._lyrics_repo.add_lyrics(new_lyrics)

    def _h5_to_dict(file) -> dict:
        with h5py.File(file, "r") as f:
            return {
                "title": f["metadata"]["songs"]["title"][0].decode("utf-8"),
                "artist": f["metadata"]["songs"]["artist_name"][0].decode("utf-8"),
                "duration": float(f["analysis"]["songs"]["duration"][0]),
                "artist_location": f["metadata"]["songs"]["artist_location"][0].decode(
                    "utf-8"
                ),
                "album": f["metadata"]["songs"]["release"][0].decode("utf-8"),
                "tempo": float(f["analysis"]["songs"]["tempo"][0]),
                "key": float(f["analysis"]["songs"]["key"][0]),
                "loudness": float(f["analysis"]["songs"]["loudness"][0]),
                "mode": float(f["analysis"]["songs"]["mode"][0]),
                "time_signature": float(f["analysis"]["songs"]["time_signature"][0]),
            }

    def _request_lyrics(artist: str, track: str) -> Optional[str]:
        base_url = f"https://api.lyrics.ovh/v1/{artist}/{track}"
        response = requests.get(base_url)

        if response.status_code == 200:
            data = response.json()
            return data.get("lyrics", None)
        else:
            return None
