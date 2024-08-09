from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Petrol(Base):
    __tablename__ = "petrol"

    id = Column(String, primary_key=True, index=True)
    type = Column(String, index=True)
    amount = Column(Float, index=True)
    gas_station_id = Column(String, ForeignKey('petrol_station.id'), index=True)
    updated = Column(Integer, index=True)

    # Define the relationship
    petrol_station = relationship('PetrolStation', back_populates='petrol_list')
