from typing import Union
import psycopg2
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


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
