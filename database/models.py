from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Artist(Base):
    __tablename__ = "artists"
    name = Column(String, primary_key=True)
    location = Column(String)

    # Relationship to Songs
    songs = relationship("Song", back_populates="artist")


class Lyrics(Base):
    __tablename__ = "lyrics"
    title = Column(String, ForeignKey("songs.title"), primary_key=True)
    lyrics = Column(String, nullable=True)

    song = relationship("Song", back_populates="lyrics")


class Song(Base):
    __tablename__ = "songs"
    title = Column(String, primary_key=True)
    artist_name = Column(String, ForeignKey("artists.name"), nullable=True)
    album_name = Column(String, ForeignKey("albums.name"), nullable=True)
    genre_name = Column(String, ForeignKey("genres.name"), nullable=True)

    # # Relationships
    artist = relationship("Artist", back_populates="songs")
    genre = relationship("Genre", back_populates="songs")
    album = relationship("Album", back_populates="songs")
    audio_feature = relationship("AudioFeature", back_populates="songs")
    lyrics = relationship("Lyrics", back_populates="song")


# Dimension Table: Genres
class Genre(Base):
    __tablename__ = "genres"
    name = Column(String, primary_key=True)

    # Relationship to Songs
    songs = relationship("Song", back_populates="genre")


# Dimension Table: Albums
class Album(Base):
    __tablename__ = "albums"
    name = Column(String, primary_key=True)

    # Relationship to Songs
    songs = relationship("Song", back_populates="album")


class AudioFeature(Base):
    __tablename__ = "audio_features"
    title = Column(String, ForeignKey("songs.title"), primary_key=True)
    tempo = Column(Float)
    key = Column(Integer)
    loudness = Column(Float)
    mode = Column(Integer)
    time_signature = Column(Integer)
    duration = Column(Float)

    songs = relationship("Song", back_populates="audio_feature")
