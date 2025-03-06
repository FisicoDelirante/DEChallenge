from fastapi import APIRouter, Depends

from controllers.querying import QueryController

__ROUTE_PREFIX__ = "/query"

router = APIRouter(prefix=__ROUTE_PREFIX__, tags=["Queries"])


@router.get("/listAllSongs")
def list_all_songs(query_controller=Depends(QueryController)):
    results = query_controller.get_all_songs()
    return {"songs": [results]}


@router.get("/listAllArtists")
def list_all_artists(query_controller=Depends(QueryController)):
    results = query_controller.get_all_artists()
    return {"artists": results}


@router.get("/listAllAlbums")
def list_all_albums(query_controller=Depends(QueryController)):
    results = query_controller.get_all_albums()
    return {"albums": results}


@router.get("/getAlbumStats")
def get_album_information(album: str, query_controller=Depends(QueryController)):
    result = query_controller.get_album_information(album)
    return {
        "albumName": result.album_name,
        "averageDuration": result.avg_duration,
        "totalSongs": result.total_songs,
    }


@router.get("/getSongByTheme")
def get_songs_by_theme(term: str, query_controller=Depends(QueryController)):
    return query_controller.semantic_search(term)


@router.get("/getSongInfo")
def get_song_information(song: str, query_controller=Depends(QueryController)):
    result = query_controller.get_song_information(song)
    return {
        "title": result.title,
        "artist_name": result.artist_name,
        "album_name": result.album_name,
        "lyrics": result.lyrics,
        "duration": result.duration,
        "key": result.key,
        "loudness": result.loudness,
        "mode": result.mode,
        "tempo": result.tempo,
        "time_signature": result.time_signature,
    }
