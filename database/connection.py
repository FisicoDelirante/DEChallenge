from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_connection_string() -> str:
    # Database Connection
    USER = config("USER")
    PASSWORD = config("PASSWORD")
    SERVER = config("SERVER")
    DB = config("DB")
    return f"postgresql://{USER}:{PASSWORD}@{SERVER}:12345/{DB}"


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
