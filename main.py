from typing import Union
import psycopg2
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Car
import typesense
from api.ingestion import router as ingestion_router

app = FastAPI()
app.include_router(ingestion_router)


@app.get("/testConnection2")
def test_sqlalchemy_connection():
    # Example of creating an engine and session
    # Replace with your database connection string
    DATABASE_URL = "postgresql://fer:pwc@localhost:12345/dechallenge"
    engine = create_engine(DATABASE_URL, echo=True)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Example: Insert some cars
    cars_to_add = [
        Car(car_model="Toyota Camry", color="Blue"),
        Car(car_model="Honda Accord", color="Red"),
        Car(car_model="Tesla Model 3", color="Black"),
        Car(car_model="Ford Mustang", color="Yellow"),
        Car(car_model="Chevrolet Malibu", color="White"),
    ]

    session.add_all(cars_to_add)
    session.commit()

    # Query the cars table
    cars = session.query(Car).all()
    for car in cars:
        print(car)


# ToDo: move these environment variables somewhere else
@app.get("/testConnection")
def test_direct_connection():
    db_config = {
        "host": "localhost",
        "port": 12345,
        "database": "dechallenge",
        "user": "fer",
        "password": "pwc",
    }

    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()[0]
    connection.close()
    return {f"Version is {db_version}"}


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
