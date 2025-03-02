from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# Define the base class
Base = declarative_base()


# Fact Table: Artists
class Artist(Base):
    __tablename__ = "artists"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String)

    # Relationship to Songs
    songs = relationship("Song", back_populates="artist")


# Fact & Dimension Table: Songs
class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    duration = Column(Float)
    play_count = Column(Integer, default=0)

    # # Relationships
    artist = relationship("Artist", back_populates="songs")
    genre = relationship("Genre", back_populates="songs")
    album = relationship("Album", back_populates="songs")


# Dimension Table: Genres
class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship to Songs
    songs = relationship("Song", back_populates="genre")


# Dimension Table: Albums
class Album(Base):
    __tablename__ = "albums"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Relationship to Songs
    songs = relationship("Song", back_populates="album")
