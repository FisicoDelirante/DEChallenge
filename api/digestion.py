import requests
from minio.commonconfig import CopySource

from fastapi import APIRouter, Depends
from minio import Minio
import io
import h5py
from sqlalchemy import Select

from database.connection import get_session
from database.models import Album, Artist, AudioFeature, Lyrics, Song

__ROUTE_PREFIX__ = "/digestion"

router = APIRouter(prefix=__ROUTE_PREFIX__)


# Open an HDF5 file from the dataset
def h5_to_dict(filename):
    with h5py.File(filename, "r") as f:
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


def add_songs_with_audio_features_bulk(session, songs):
    # 1. Extract unique artists and albums from the list
    artist_names = {song["artist"] for song in songs}
    album_names = {song["album"] for song in songs if song.get("album")}
    # genre should also be here

    # 2. Query existing artists and albums
    existing_artists = session.query(Artist).all()
    existing_albums = session.query(Album).all()

    # 3. Keep only new artists
    new_artists = artist_names - {artist.name for artist in existing_artists}
    new_albums = album_names - {album.name for album in existing_albums}

    # 4. Insert missing artists (using artist_location for the 'country' field)
    new_artists_db = []
    for name in new_artists:
        # Use the first occurrence of the artist's location
        location = next(
            (song["artist_location"] for song in songs if song["artist"] == name),
            None,
        )
        new_artist = Artist(name=name, location=location)
        new_artists_db.append(new_artist)
    if new_artists:
        session.add_all(new_artists_db)

    # 5. Insert missing albums
    new_albums_db = [Album(name=name) for name in new_albums]
    if new_albums_db:
        session.add_all(new_albums_db)

    # 6. Prepare Song and AudioFeature records for each song in the list
    new_songs = []
    new_features = []
    for song in songs:

        # Create a new AudioFeature record (one per song)
        audio_feature = AudioFeature(
            title=song["title"],
            tempo=song["tempo"],
            key=song["key"],
            loudness=song["loudness"],
            mode=song["mode"],
            time_signature=song["time_signature"],
            duration=song["duration"],
        )
        new_features.append(audio_feature)

        # Create the Song record with foreign key references
        new_song = Song(
            title=song["title"],
            artist_name=song["artist"],
            album_name=song["album"],
        )
        new_songs.append(new_song)

    # 7. Bulk insert all Song records and commit once
    session.add_all(new_songs)
    session.add_all(new_features)
    session.commit()
    print(f"Successfully added {len(new_songs)} songs.")


@router.post("/processFile")
def process_files(session=Depends(get_session)):
    # ToDo move to a different file
    minio_client = Minio(
        "localhost:9000",  # MinIO address
        access_key="admin",
        secret_key="password",
        secure=False,  # Set to True if using HTTPS
    )
    source_bucket = "my-bucket"
    destination_bucket = "processed"
    processed_files = []
    for f in minio_client.list_objects(source_bucket):
        # Download the file
        response = minio_client.get_object(source_bucket, f.object_name)
        file_data = io.BytesIO(response.data)
        processed_files.append(h5_to_dict(file_data))
        cs = CopySource(source_bucket, f.object_name)
        try:
            # Copy the object to the destination bucket
            minio_client.copy_object(destination_bucket, f.object_name, cs)
            print(
                f"Copied {f.object_name} from {source_bucket} to {destination_bucket}."
            )

            # Remove the object from the source bucket
            minio_client.remove_object(source_bucket, f.object_name)
            print(f"Removed {f.object_name} from {source_bucket}.")

        except Exception as err:
            print("Error occurred:", err)

    add_songs_with_audio_features_bulk(session, processed_files)


def get_lyrics_no_api_key(artist, track):
    # Format the URL: artist and track should be
    # URL-encoded if they contain special characters.
    base_url = f"https://api.lyrics.ovh/v1/{artist}/{track}"
    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()
        return data.get("lyrics", None)
    else:
        return None


@router.post("/processLyrics")
def add_lyrics(session=Depends(get_session)):
    statement = Select(Song.title, Song.artist_name).where(
        Song.title.not_in(Select(Lyrics.title))
    )
    songs_without_lyrics = session.execute(statement).all()
    new_lyrics = []
    for song in songs_without_lyrics:
        lyrics = get_lyrics_no_api_key(song.artist_name, song.title)
        new_lyrics.append(Lyrics(title=song.title, lyrics=lyrics))
    session.add_all(new_lyrics)
    session.commit()
