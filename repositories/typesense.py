from fastapi import Depends
import typesense


def get_typesense_client():
    return typesense.Client(
        {
            "nodes": [
                {
                    "host": "localhost",
                    "port": "8108",
                    "protocol": "http",
                }
            ],
            "api_key": "xyz",
            "connection_timeout_seconds": 2,
        }
    )


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
