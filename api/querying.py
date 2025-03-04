from fastapi import APIRouter
import typesense

__ROUTE_PREFIX__ = "/query"

router = APIRouter(prefix=__ROUTE_PREFIX__)


client = typesense.Client(
    {
        "nodes": [{"host": "localhost", "port": "8108", "protocol": "http"}],
        "api_key": "xyz",
        "connection_timeout_seconds": 2,
    }
)


@router.get("/getSongInfo")
def upload_h5_file():
    pass


@router.get("/getAllSongs")
def whatever():
    pass


@router.get("/getSongByTheme")
def get_songs_by_theme(term: str):
    response = client.collections["songs"].documents.search(
        {
            "q": term,
            "query_by": "embedding",
            "exclude_fields": "embedding",
        }
    )
    return response
