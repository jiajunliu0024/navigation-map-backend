from pydantic import BaseModel


class PetrolBase(BaseModel):
    id: str
    gas_station_id: str
    type: str
    updated: int
    amount: float

    class Config:
        from_attributes = True


class PetrolCreateOrUpdate(PetrolBase):
    pass


class Petrol(PetrolBase):
    id: str

    class Config:
        from_attributes = True




