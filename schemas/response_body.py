from pydantic import BaseModel
from typing import List, Any
from schemas.petrol_station_schema import PetrolStation


class ResponseBody(BaseModel):
    message: str
    size: int
    body: List[PetrolStation]
    code: int
