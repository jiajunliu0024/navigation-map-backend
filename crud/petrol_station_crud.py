from sqlalchemy import and_, or_
from sqlalchemy.orm import Session, joinedload

import schemas
from schemas import petrol_station_schema
from models.petrol_station_model import PetrolStation
from schemas.bounding_box import BoundingBox
from schemas.petrol_station_schema import PetrolStationWithPetrol


def get_petrol_station_id(db: Session, petrol_station_id: int):
    return db.query(PetrolStation).options(joinedload
                                           (PetrolStation.petrol_list)).filter(
        PetrolStation.id.__eq__(petrol_station_id)).first()


def get_petrol_station_by_bounding_box(db: Session, box: BoundingBox):
    petrol_stations = db.query(PetrolStation).options(joinedload(PetrolStation.petrol_list)).filter(
        and_(
            PetrolStation.location_y >= box.sw_lat,
            PetrolStation.location_y <= box.ne_lat,
            PetrolStation.location_x >= box.sw_lng,
            PetrolStation.location_x <= box.ne_lng
        )
    ).all()
    return petrol_stations


def get_petrol_station_by_bounding_boxes_paginated(db: Session, boxes: list, batch_size: int = 50):
    petrol_station_box_list = []

    for i in range(0, len(boxes), batch_size):
        batch = boxes[i:i + batch_size]

        conditions = [
            and_(
                PetrolStation.location_y >= box.sw_lat,
                PetrolStation.location_y <= box.ne_lat,
                PetrolStation.location_x >= box.sw_lng,
                PetrolStation.location_x <= box.ne_lng
            )
            for box in batch
        ]

        query = db.query(PetrolStation).filter(or_(*conditions))
        batch_results = query.all()
        petrol_station_box_list.extend(batch_results)

    # Remove duplicates from the result list
    unique_petrol_station_box_list = list({station.id: station for station in petrol_station_box_list}.values())

    return unique_petrol_station_box_list


def page_petrol_station(db: Session, skip: int = 0, limit: int = 10):
    return db.query(PetrolStation).offset(skip).limit(limit).all()


def create_petrol_station(db: Session, petrol_station: petrol_station_schema.PetrolStationCreateOrUpdate):
    # Convert Pydantic model to dictionary
    station_data = petrol_station.model_dump()
    
    # Create SQLAlchemy model instance
    db_station = PetrolStation(**station_data)
    db.add(db_station)
    db.commit()
    db.refresh(db_station)
    return db_station


def update_petrol_station(db: Session, petrol_station_id: int,
                          petrol_station: petrol_station_schema.PetrolStationCreateOrUpdate):
    db_petrol_station = db.query(PetrolStation).filter(PetrolStation.id == petrol_station_id).first()
    if db_petrol_station:
        for key, value in petrol_station.dict().items():
            if key != 'petrol_list':
                setattr(db_petrol_station, key, value)
        db.commit()
        db.refresh(db_petrol_station)
        return db_petrol_station
    print("update petrol station")
    return None


def delete_petrol_station(db: Session, petrol_station_id: int):
    db_petrol = db.query(PetrolStation).filter(PetrolStation.id == petrol_station_id).first()
    if db_petrol:
        db.delete(db_petrol)
        db.commit()
        return db_petrol
    return None
