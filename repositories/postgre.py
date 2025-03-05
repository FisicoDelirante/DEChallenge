from fastapi import Depends
from sqlalchemy import Select, func
from database.connection import get_session
from database.models import (
    Album,
    Artist,
    AudioFeature,
    GoldAlbumPerformance,
    GoldArtistPerformance,
    Lyrics,
    Song,
)


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


class GoldRepo:
    def __init__(self, session=Depends(get_session)):
        self._session = session

    def update_gold_artist_performance(self):
        """
        Aggregates artist performance metrics and updates
        the gold_artist_performance table.
        """
        # Query: join Artist, Song, and AudioFeature to compute aggregates
        artist_data = (
            self._session.query(
                Artist.name.label("artist_name"),
                func.count(Song.title).label("total_songs"),
                func.avg(AudioFeature.tempo).label("avg_tempo"),
                func.avg(AudioFeature.loudness).label("avg_loudness"),
                func.sum(AudioFeature.duration).label("total_duration"),
            )
            .join(Song, Song.artist_name == Artist.name)
            .join(AudioFeature, AudioFeature.title == Song.title)
            .group_by(Artist.name)
            .all()
        )

        # Optionally clear out existing records
        self._session.query(GoldArtistPerformance).delete()

        # Insert aggregated data into GoldArtistPerformance
        for row in artist_data:
            performance = GoldArtistPerformance(
                artist_name=row.artist_name,
                total_songs=row.total_songs,
                avg_tempo=row.avg_tempo,
                avg_loudness=row.avg_loudness,
                total_duration=row.total_duration,
            )
            self._session.add(performance)
        self._session.commit()
        print("GoldArtistPerformance updated.")

    def update_gold_album_performance(self):
        """
        Aggregates album performance metrics and updates the
        gold_album_performance table.
        """
        album_data = (
            self._session.query(
                Album.name.label("album_name"),
                func.count(Song.title).label("total_songs"),
                func.avg(AudioFeature.duration).label("avg_duration"),
            )
            .join(Song, Song.album_name == Album.name)
            .join(AudioFeature, AudioFeature.title == Song.title)
            .group_by(Album.name)
            .all()
        )

        self._session.query(GoldAlbumPerformance).delete()

        for row in album_data:
            performance = GoldAlbumPerformance(
                album_name=row.album_name,
                total_songs=row.total_songs,
                avg_duration=row.avg_duration,
            )
            self._session.add(performance)
        self._session.commit()
        print("GoldAlbumPerformance updated.")
