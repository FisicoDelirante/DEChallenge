from typing import Union
import psycopg2
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Car

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


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
