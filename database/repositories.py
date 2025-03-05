from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

# Import your models (assuming they are defined in a module named models)
from models import (
    Artist,
    Song,
    AudioFeature,
    Album,
    GoldArtistPerformance,
    GoldAlbumPerformance,
)


# Create engine and session (update the connection string as needed)
engine = create_engine("postgresql://fer:pwc@localhost:12345/dechallenge")
Session = sessionmaker(bind=engine)
session = Session()


def update_gold_artist_performance(session):
    """
    Aggregates artist performance metrics and updates the gold_artist_performance table.
    """
    # Query: join Artist, Song, and AudioFeature to compute aggregates
    artist_data = (
        session.query(
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
    session.query(GoldArtistPerformance).delete()

    # Insert aggregated data into GoldArtistPerformance
    for row in artist_data:
        performance = GoldArtistPerformance(
            artist_name=row.artist_name,
            total_songs=row.total_songs,
            avg_tempo=row.avg_tempo,
            avg_loudness=row.avg_loudness,
            total_duration=row.total_duration,
        )
        session.add(performance)
    session.commit()
    print("GoldArtistPerformance updated.")


def update_gold_album_performance(session):
    """
    Aggregates album performance metrics and updates the gold_album_performance table.
    """
    album_data = (
        session.query(
            Album.name.label("album_name"),
            func.count(Song.title).label("total_songs"),
            func.avg(AudioFeature.duration).label("avg_duration"),
        )
        .join(Song, Song.album_name == Album.name)
        .join(AudioFeature, AudioFeature.title == Song.title)
        .group_by(Album.name)
        .all()
    )

    session.query(GoldAlbumPerformance).delete()

    for row in album_data:
        performance = GoldAlbumPerformance(
            album_name=row.album_name,
            total_songs=row.total_songs,
            avg_duration=row.avg_duration,
        )
        session.add(performance)
    session.commit()
    print("GoldAlbumPerformance updated.")


# def refresh_gold_song_details(session):
#     """
#     Refreshes the materialized view 'gold_song_details'.
#     This is PostgreSQL specific.
#     """
#     session.execute("REFRESH MATERIALIZED VIEW gold_song_details;")
#     session.commit()
#     print("Materialized view 'gold_song_details' refreshed.")


if __name__ == "__main__":
    # Run the transformations
    update_gold_artist_performance(session)
    update_gold_album_performance(session)
    # refresh_gold_song_details(session)
