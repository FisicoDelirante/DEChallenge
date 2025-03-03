from fastapi import FastAPI
import typesense
from api.ingestion import router as ingestion_router
from api.digestion import router as digestion_router

app = FastAPI()
app.include_router(ingestion_router)
app.include_router(digestion_router)


@app.get("/testVectorDB")
def test_direct_connection():
    client = typesense.Client(
        {
            "nodes": [
                {
                    "host": "localhost",  # For Typesense Cloud use xxx.a1.typesense.net
                    "port": "8108",  # For Typesense Cloud use 443
                    "protocol": "http",  # For Typesense Cloud use https
                }
            ],
            "api_key": "xyz",
            "connection_timeout_seconds": 2,
        }
    )
    # teswt
    books_schema = {
        "name": "books",
        "fields": [
            {"name": "title", "type": "string"},
            {"name": "authors", "type": "string[]", "facet": True},
            {"name": "publication_year", "type": "int32", "facet": True},
            {"name": "ratings_count", "type": "int32"},
            {"name": "average_rating", "type": "float"},
        ],
        "default_sorting_field": "ratings_count",
    }

    # client.collections.create(books_schema)

    # with open("typesense-data/books.jsonl") as jsonl_file:
    #     client.collections["books"].documents.import_(jsonl_file.read().encode("utf-8"))
    # return
    search_parameters = {
        "q": "harry potter",
        "query_by": "title",
        "sort_by": "ratings_count:desc",
    }

    return client.collections["books"].documents.search(search_parameters)
