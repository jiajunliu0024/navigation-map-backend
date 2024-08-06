from pydantic import BaseModel


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


class PetrolStationCreateOrUpdate(PetrolStationBase):
    pass


class PetrolStationCreate(PetrolStationBase):
    pass


class PetrolStation(PetrolStationBase):
    class Config:
        from_attributes = True
