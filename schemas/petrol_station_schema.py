from typing import List

from pydantic import BaseModel, Field

from schemas.petrol_price_schema import Petrol


class PetrolStationBase(BaseModel):
    id: str
    name: str
    brand: str
    state: str
    suburb: str
    address: str
    postcode: str = Field(alias="postCode")
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

    class Config:
        from_attributes = True
        populate_by_name = True


class PetrolStationCreateOrUpdate(PetrolStationBase):
    pass


class PetrolStationCreate(PetrolStationBase):
    pass


class PetrolStation(PetrolStationBase):
    class Config:
        from_attributes = True


class PetrolStationWithPetrol(PetrolStationBase):
    petrol_list: list


class RouteCoordinates(BaseModel):
    src_lat: float = Field(..., alias="srcLat", description="Source latitude")
    src_lng: float = Field(..., alias="srcLng", description="Source longitude")
    des_lat: float = Field(..., alias="desLat", description="Destination latitude")
    des_lng: float = Field(..., alias="desLng", description="Destination longitude")


class MapBoundaries(BaseModel):
    sw_lat: float = Field(..., alias="swLat", description="Southwest latitude")
    sw_lng: float = Field(..., alias="swLng", description="Southwest longitude")
    ne_lat: float = Field(..., alias="neLat", description="Northeast latitude")
    ne_lng: float = Field(..., alias="neLng", description="Northeast longitude")
