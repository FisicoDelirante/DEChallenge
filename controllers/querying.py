from fastapi import Depends
from repositories.postgre import AlbumsRepo, ArtistsRepo, GoldRepo, SongsRepo
from repositories.typesense import TypesenseRepo
from sqlalchemy.exc import NoResultFound


class QueryController:

    def __init__(
        self,
        typesense_repo=Depends(TypesenseRepo),
        songs_repo=Depends(SongsRepo),
        albums_repo=Depends(AlbumsRepo),
        artists_repo=Depends(ArtistsRepo),
        gold_repo=Depends(GoldRepo),
    ):
        self._typesense_repo = typesense_repo
        self._songs_repo = songs_repo
        self._albums_repo = albums_repo
        self._artists_repo = artists_repo
        self._gold_repo = gold_repo

    def semantic_search(self, query: str, results_number: int = 10) -> list[dict]:
        songs = []
        for results_page in self._typesense_repo.semantic_search(
            "songs", query, results_number
        ):
            for hit in results_page["hits"]:
                songs.append(
                    {
                        "title": hit["document"]["title"],
                        "lyrics": hit["document"]["lyrics"],
                        "artist": hit["document"]["artist"],
                    }
                )
        return songs

    def get_album_information(self, album: str):
        try:
            return self._gold_repo.get_album_performance(album)[0]
        except NoResultFound:
            return None

    def get_song_information(self, album: str):
        try:
            return self._songs_repo.get_song_with_info(album)
        except NoResultFound:
            return None

    def get_all_songs(self):
        return [song.title for song in self._songs_repo.get_all_songs()]

    def get_all_artists(self):
        return [artist.name for artist in self._artists_repo.get_all_artists()]

    def get_all_albums(self):
        return [album.name for album in self._albums_repo.get_all_albums()]
