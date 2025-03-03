from sqlalchemy import Insert, Select
from database.connection import get_session
from database.models import Album, Artist, Genre, Song


def get_all_songs():
    g = get_session()
    session = next(g)
    statement = Select(Song.album, Song.artist)
    return session.execute(statement).all()


def add_song(
    title,
    artist_name,
    genre_name,
    album_name=None,
    duration=None,
    play_count=0,
):
    g = get_session()
    session = next(g)

    # Check if the artist already exists
    artist = session.query(Artist).filter_by(name=artist_name).first()

    if not artist:
        # Create new artist
        artist = Artist(name=artist_name)
        session.add(artist)
        session.commit()  # Commit to get the artist ID

    # Check if the genre exists
    genre = session.query(Genre).filter_by(name=genre_name).first()
    if not genre:
        genre = Genre(name=genre_name)
        session.add(genre)
        session.commit()

    # Check if the album exists (optional)
    album = None
    if album_name:
        album = session.query(Album).filter_by(name=album_name).first()
        if not album:
            album = Album(name=album_name)
            session.add(album)
            session.commit()

    # Create the song
    song = Song(
        title=title,
        artist_id=artist.id,
        genre_id=genre.id,
        album_id=album.id if album else None,
        duration=duration,
        play_count=play_count,
    )

    # Add to session and commit
    session.add(song)
    session.commit()

    print(f"Added song: {title} by {artist_name}")


if __name__ == "__main__":
    # Example Usage
    add_song(
        "Bohemian Rhapsody",
        "Queen",
        "Rock",
        album_name="A Night at the Opera",
        duration=5.55,
        play_count=100,
    )
