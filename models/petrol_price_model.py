from sqlalchemy import Column, Integer, String, Float
from database import Base


class Petrol(Base):
    __tablename__ = "petrol"

    id = Column(String, primary_key=True, index=True)
    type = Column(String, index=True)
    amount = Column(Float, index=True)
    gas_station_id = Column(String, index=True)
    updated = Column(Integer, index=True)
