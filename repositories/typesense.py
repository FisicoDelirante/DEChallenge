from math import ceil
from fastapi import Depends

from database.connection import get_typesense_client


class TypesenseRepo:
    RESULTS_PER_PAGE = 50

    def __init__(self, typesense_client=Depends(get_typesense_client)):
        self.typesense_client = typesense_client

    def bulk_upload(self, collection: str, documents: list[dict]):
        self.typesense_client.collections[collection].documents.import_(
            documents, {"action": "upsert"}
        )

    def semantic_search(
        self, collection: str, query: str, results_number: int = 10
    ) -> list[dict]:
        if results_number > self.RESULTS_PER_PAGE:
            return self._make_paginated_search(collection, query, results_number)
        response = self.typesense_client.collections[collection].documents.search(
            {
                "q": query,
                "query_by": "embedding",
                "exclude_fields": "embedding",
                "limit": results_number,
            }
        )
        return [response]

    def check_if_collection_exists(self, collection: str) -> bool:
        existing_collections = self.typesense_client.collections.retrieve()
        collections_names = {c["name"] for c in existing_collections}
        return collection in collections_names

    def create_schema(self, schema: dict) -> None:
        self.typesense_client.collections.create(schema)

    def _make_paginated_search(
        self, collection: str, query: str, results_number: int
    ) -> list[dict]:
        pages = ceil(results_number / self.RESULTS_PER_PAGE)
        responses = [
            self.typesense_client.collections[collection].documents.search(
                {
                    "q": query,
                    "query_by": "embedding",
                    "exclude_fields": "embedding",
                    "per_page": self.RESULTS_PER_PAGE,
                    "limit": results_number,
                    "page": i,
                }
            )
            for i in range(pages + 1)
        ]
        return responses
