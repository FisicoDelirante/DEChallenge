from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Define the base class
Base = declarative_base()


# Fact Table: Artists
class Artist(Base):
    __tablename__ = "artists"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String)

    # Relationship to Songs
    songs = relationship("Song", back_populates="artist")


# Fact & Dimension Table: Songs
class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    lyrics = Column(String, nullable=True)
    duration = Column(Float)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    audio_feature_id = Column(Integer, ForeignKey("audio_features.id"), nullable=True)

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


class AudioFeature(Base):
    __tablename__ = "audio_features"
    id = Column(Integer, primary_key=True)
    tempo = Column(Float)
    key = Column(Integer)
    loudness = Column(Float)
    mode = Column(Integer)
    time_signature = Column(Integer)
    # You can add additional fields if available, e.g., danceability, energy, etc.

    # Relationship to songs (one-to-many if different songs share similar features)
    songs = relationship("Song", back_populates="audio_feature")
