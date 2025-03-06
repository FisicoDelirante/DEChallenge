from decouple import config
from minio import Minio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import typesense


# Postgre
def get_connection_string() -> str:
    # Database Connection
    USER = config("USER")
    PASSWORD = config("PASSWORD")
    SERVER = config("SERVER")
    DB = config("DB")
    return f"postgresql://{USER}:{PASSWORD}@{SERVER}/{DB}"


def engine_maker():
    connection_string = get_connection_string()
    engine = create_engine(connection_string)
    return engine


engine = engine_maker()
SessionLocal = sessionmaker(bind=engine)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Minio
def get_minio_client():
    return Minio(
        config("MINIO_HOST"),
        access_key=config("MINIO_USER"),
        secret_key=config("MINIO_PASSWORD"),
        secure=False,
    )


# Typesense
def get_typesense_client():
    return typesense.Client(
        {
            "nodes": [
                {
                    "host": config("TS_HOST"),
                    "port": config("TS_PORT"),
                    "protocol": "http",
                }
            ],
            "api_key": config("TS_KEY"),
            "connection_timeout_seconds": 30,
        }
    )
