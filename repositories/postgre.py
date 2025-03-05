from fastapi import Depends
from sqlalchemy import Select
from database.connection import get_session
from database.models import Album, Artist, AudioFeature, Lyrics, Song


class SongsRepo:
    def __init__(self, session=Depends(get_session)):
        self._session = session

    def get_songs_without_lyrics(self):
        """Note that songs with lyrics=None are considered already processed,
        since this data isn't available for all songs"""
        statement = Select(Song.title, Song.artist_name).where(
            Song.title.not_in(Select(Lyrics.title))
        )
        return self._session.execute(statement).all()

    def add_songs_with_features(self, songs: list[dict]):
        # So far I'm assuming a song will be uploaded only once.
        # I should fix it, but first I need to get everything running.
        # Extract unique artists and albums from the list
        artist_names = {song["artist"] for song in songs}
        album_names = {song["album"] for song in songs if song.get("album")}
        # genre should also be here

        # Query existing artists and albums
        existing_artists = self._session.query(Artist).all()
        existing_albums = self._session.query(Album).all()

        # Keep only new artists and new albums
        new_artists = artist_names - {artist.name for artist in existing_artists}
        new_albums = album_names - {album.name for album in existing_albums}

        # Insert missing artists
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
            self._session.add_all(new_artists_db)

        # Insert missing albums
        new_albums_db = [Album(name=name) for name in new_albums]
        if new_albums_db:
            self._session.add_all(new_albums_db)

        # Prepare Song and AudioFeature records for each song in the list
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
        self._session.add_all(new_songs)
        self._session.add_all(new_features)
        self._session.commit()
        print(f"Successfully added {len(new_songs)} songs.")

    def get_songs_with_artist_and_lyrics(self):
        return (
            self._session.query(Song.artist_name, Song.title, Lyrics.lyrics)
            .join(Lyrics, Song.title == Lyrics.title)
            .filter(Lyrics.lyrics != None)  # noqa
            .all()
        )


class LyricsRepo:
    def __init__(self, session=Depends(get_session)):
        self._session = session

    def add_lyrics(self, lyrics: list[dict]) -> None:
        self._session.add_all([Lyrics(**lyrics_dict) for lyrics_dict in lyrics])
        self._session.commit()


class ArtistsRepo:
    def __init__(self, session=Depends(get_session)):
        self._session = session

    def get_all_artists(self):
        return self._session.query(Artist).all()


class AlbumsRepo:
    def __init__(self, session=Depends(get_session)):
        self._session = session

    def get_all_albums(self):
        return self._session.query(Album).all()
