from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import petrol_price_schema
from crud import petrol_price_crud
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/petrol/", response_model=petrol_price_schema.Petrol)
def create_petrol(petrol: petrol_price_schema.PetrolCreateOrUpdate, db: Session = Depends(get_db)):
    return petrol_price_crud.create_petrol(db=db, petrol=petrol)


@router.get("/petrol/{petrol_id}", response_model=petrol_price_schema.Petrol)
def read_petrol(petrol_id: int, db: Session = Depends(get_db)):
    db_petrol = petrol_price_crud.get_petrol(db, petrol_id=petrol_id)
    if db_petrol is None:
        raise HTTPException(status_code=404, detail="Petrol not found")
    return db_petrol


@router.get("/petrol/", response_model=list[petrol_price_schema.Petrol])
def read_list_petrol(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return petrol_price_crud.page_petrol(db, skip=skip, limit=limit)


@router.delete("/petrol/{petrol_id}", response_model=petrol_price_schema.Petrol)
def delete_petrol(petrol_id: int, db: Session = Depends(get_db)):
    deleted_petrol = petrol_price_crud.delete_petrol(db, petrol_id)
    if deleted_petrol is None:
        raise HTTPException(status_code=404, detail="Petrol not found")
    return deleted_petrol
