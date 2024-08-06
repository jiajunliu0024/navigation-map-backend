from sqlalchemy import and_
from sqlalchemy.orm import Session

import schemas
from schemas import petrol_station_schema
from models.petrol_station_model import PetrolStation
from schemas.bounding_box import BoundingBox


def get_petrol_station_id(db: Session, petrol_station_id: int):
    return db.query(PetrolStation).filter(PetrolStation.id == petrol_station_id).first()


def get_petrol_station_by_bounding_box(db: Session, box: BoundingBox):
    petrol_stations = db.query(PetrolStation).filter(
        and_(
            PetrolStation.location_y >= box.sw_lat,
            PetrolStation.location_y <= box.ne_lat,
            PetrolStation.location_x >= box.sw_lng,
            PetrolStation.location_x <= box.ne_lng
        )
    ).all()
    return petrol_stations


def page_petrol_station(db: Session, skip: int = 0, limit: int = 10):
    return db.query(PetrolStation).offset(skip).limit(limit).all()


def create_petrol_station(db: Session, petrol_station: petrol_station_schema.PetrolStationCreateOrUpdate):
    db_petrol_station = PetrolStation(**petrol_station.dict())
    db.add(db_petrol_station)
    db.commit()
    db.refresh(db_petrol_station)
    return db_petrol_station


def update_petrol_station(db: Session, petrol_station_id: int,
                          petrol_station: petrol_station_schema.PetrolStationCreateOrUpdate):
    db_petrol_station = db.query(PetrolStation).filter(PetrolStation.id == petrol_station_id).first()
    if db_petrol_station:
        for key, value in petrol_station.dict().items():
            setattr(db_petrol_station, key, value)
        db.commit()
        db.refresh(db_petrol_station)
        return db_petrol_station
    return None


def delete_petrol_station(db: Session, petrol_station_id: int):
    db_petrol = db.query(PetrolStation).filter(PetrolStation.id == petrol_station_id).first()
    if db_petrol:
        db.delete(db_petrol)
        db.commit()
        return db_petrol
    return None
