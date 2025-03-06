from fastapi import Depends

from database.connection import get_typesense_client


class TypesenseRepo:

    def __init__(self, typesense_client=Depends(get_typesense_client)):
        self.typesense_client = typesense_client

    def bulk_upload(self, collection: str, documents: list[dict]):
        self.typesense_client.collections[collection].documents.import_(
            documents, {"action": "upsert"}
        )

    def semantic_search(self, collection: str, query: str):
        response = self.typesense_client.collections[collection].documents.search(
            {
                "q": query,
                "query_by": "embedding",
                "exclude_fields": "embedding",
            }
        )
        return response

    def check_if_collection_exists(self, collection: str) -> bool:
        existing_collections = self.typesense_client.collections.retrieve()
        collections_names = {c["name"] for c in existing_collections}
        return collection in collections_names

    def create_schema(self, schema: dict):
        self.typesense_client.collections.create(schema)
