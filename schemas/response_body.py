from pydantic import BaseModel
from typing import List, Any, Union, Dict
from schemas.petrol_station_schema import PetrolStation


class ResponseBody(BaseModel):
    message: str
    size: int
    body: Union[List[PetrolStation], Dict[str, Any]]
    code: int
