from typing import List

from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

from database import Base


class PetrolStation(Base):
    __tablename__ = 'petrol_station'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    state = Column(String, nullable=False)
    suburb = Column(String, nullable=False)
    address = Column(String, nullable=False)
    postcode = Column(String)
    country = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    location_x = Column(Float, nullable=False)
    location_y = Column(Float, nullable=False)
    eft_ops = Column(String, nullable=False)
    truck_park = Column(String, nullable=False)
    restrooms = Column(String, nullable=False)
    accessible = Column(String, nullable=False)
    open24 = Column(String, nullable=False)
    petrol_list = relationship('Petrol', back_populates='petrol_station')
