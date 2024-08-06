from pydantic import BaseModel


class BoundingBox(BaseModel):
    ne_lat: float
    ne_lng: float
    sw_lat: float
    sw_lng: float
