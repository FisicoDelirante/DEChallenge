from fastapi import APIRouter, Depends

from controllers.querying import QueryController

__ROUTE_PREFIX__ = "/query"

router = APIRouter(prefix=__ROUTE_PREFIX__, tags=["Queries"])


@router.get("/getSongInfo")
def upload_h5_file():
    pass


@router.get("/getAllSongs")
def whatever():
    pass


@router.get("/getSongByTheme")
def get_songs_by_theme(term: str, query_controller=Depends(QueryController)):
    return query_controller.semantic_search(term)
