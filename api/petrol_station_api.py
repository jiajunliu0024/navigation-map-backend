from contextlib import asynccontextmanager

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from schemas import petrol_station_schema
from crud import petrol_station_crud
from database import engine, SessionLocal, Base
from schemas.bounding_box import BoundingBox
from schemas.response_body import ResponseBody
from services.petrol_station_service import get_station_by_bounding_boxes

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/petrolStation/", response_model=petrol_station_schema.PetrolStation)
def create_petrol_station(petrol_station: petrol_station_schema.PetrolStationCreateOrUpdate,
                          db: Session = Depends(get_db)):
    return petrol_station_crud.create_petrol_station(db=db, petrol_station=petrol_station)


@router.get("/petrolStation/{petrol_station_id}", response_model=petrol_station_schema.PetrolStation)
def read_petrol_station(petrol_station_id: int, db: Session = Depends(get_db)):
    db_petrol_station = petrol_station_crud.get_petrol_station_id(db, petrol_station_id=petrol_station_id)
    if read_petrol_station is None:
        raise HTTPException(status_code=404, detail="Petrol not found")
    return read_petrol_station


@router.get("/petrol-station/bounding-boxes")
def get_petrol_station_by_box(petrol_station_box_list: list,
                              db: Session = Depends(get_db)):
    petrol_station_box_list = get_station_by_bounding_boxes(db, petrol_station_box_list)
    print(petrol_station_box_list)
    result = ResponseBody(body=petrol_station_box_list, size=len(petrol_station_box_list), message="success",
                          code=200)

    return result


@router.get("/petrolStation/", response_model=list[petrol_station_schema.PetrolStation])
def page_petrol_station(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return petrol_station_crud.page_petrol_station(db, skip=skip, limit=limit)


@router.put("/petrolStation/{petrol_station_id}", response_model=petrol_station_schema.PetrolStation)
def update_petrol(petrol_station_id: int, petrol_station: petrol_station_schema.PetrolStationCreateOrUpdate,
                  db: Session = Depends(get_db)):
    updated_petrol_station = petrol_station_crud.update_petrol_station(db, petrol_station_id, petrol_station)
    if updated_petrol_station is None:
        raise HTTPException(status_code=404, detail="Petrol not found")
    return updated_petrol_station


@router.delete("/petrolStation/{petrol_station_id}", response_model=petrol_station_schema.PetrolStation)
def delete_petrol(petrol_station_id: int, db: Session = Depends(get_db)):
    deleted_petrol_station = petrol_station_crud.delete_petrol_station(db, petrol_station_id)
    if deleted_petrol_station is None:
        raise HTTPException(status_code=404, detail="Petrol not found")
    return deleted_petrol_station
