from typing import List

from pydantic import BaseModel

from schemas.petrol_price_schema import Petrol


class PetrolStationBase(BaseModel):
    id: str
    name: str
    brand: str
    state: str
    suburb: str
    address: str
    postCode: str
    country: str
    phone: str
    location_x: float
    location_y: float
    eft_ops: bool
    truck_park: bool
    restrooms: bool
    accessible: bool
    open24: bool
    petrol_list: List[Petrol]


class PetrolStationCreateOrUpdate(PetrolStationBase):
    pass


class PetrolStationCreate(PetrolStationBase):
    pass


class PetrolStation(PetrolStationBase):
    class Config:
        from_attributes = True


class PetrolStationWithPetrol(PetrolStationBase):
    petrol_list: list
