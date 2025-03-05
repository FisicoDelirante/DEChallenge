from fastapi import Depends
from repositories.typesense import TypesenseRepo


class QueryController:

    def __init__(self, typesense_repo=Depends(TypesenseRepo)):
        self._typesense_repo = typesense_repo

    def semantic_search(self, query: str):
        return self._typesense_repo.semantic_search("songs", query)
