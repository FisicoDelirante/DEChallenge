from fastapi import APIRouter, Depends

from controllers.digestion import DigestionController

__ROUTE_PREFIX__ = "/digestion"

router = APIRouter(prefix=__ROUTE_PREFIX__)


@router.post("/processFile")
def process_files(digestion_controller=Depends(DigestionController)):
    digestion_controller.process_h5_files_in_bucket()
    return


@router.post("/processLyrics")
def add_lyrics(digestion_controller=Depends(DigestionController)):
    digestion_controller.add_lyrics()
    return


@router.post("/populateTypesense")
def populate_typesense(digestion_controller=Depends(DigestionController)):
    digestion_controller.populate_typesense()
    return


@router.post("/updateGoldLayer")
def update_gold_layer(digestion_controller=Depends(DigestionController)):
    digestion_controller.update_gold_layer()
    return
