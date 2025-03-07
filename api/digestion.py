from fastapi import APIRouter, Depends

from controllers.digestion import DigestionController

__ROUTE_PREFIX__ = "/digestion"

router = APIRouter(prefix=__ROUTE_PREFIX__, tags=["File processing"])


@router.post("/processFiles")
def process_files(digestion_controller=Depends(DigestionController)):
    """Trigger processing of unprocessed raw files. Once done,
    files will be moved to a bucket called processed."""
    digestion_controller.process_h5_files_in_bucket()
    digestion_controller.process_json_files_in_bucket()
    return


@router.post("/processLyrics")
def add_lyrics(digestion_controller=Depends(DigestionController)):
    """Check songs without lyrics, and make API requests to insert
    that data whenever possible."""
    digestion_controller.add_lyrics()
    return


@router.post("/populateTypesense")
def populate_typesense(digestion_controller=Depends(DigestionController)):
    """Insert songs with lyrics in the typesense database,
    to allow semantic searching."""
    digestion_controller.populate_typesense()
    return


@router.post("/updateGoldLayer")
def update_gold_layer(digestion_controller=Depends(DigestionController)):
    digestion_controller.update_gold_layer()
    return
