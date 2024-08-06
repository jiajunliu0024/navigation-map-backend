from pydantic import BaseModel


class PetrolBase(BaseModel):
    id: str
    type: str
    amount: float
    gas_station_id: str
    updated: int


class PetrolCreateOrUpdate(PetrolBase):
    pass


class Petrol(PetrolBase):
    id: str

    class Config:
        from_attributes = True




