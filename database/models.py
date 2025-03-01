from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker

# Define the base class
Base = declarative_base()


# Define the Car model
class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    car_model = Column(String(100), nullable=False)
    color = Column(String(50), nullable=False)

    def __repr__(self):
        return (
            f"<Car(id={self.id}, car_model='{self.car_model}', color='{self.color}')>"
        )
