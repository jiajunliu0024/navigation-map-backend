from sqlalchemy.orm import Session
from models import petrol_price_model
from schemas import petrol_price_schema


def get_petrol(db: Session, petrol_id: int):
    return db.query(petrol_price_model.Petrol).filter(petrol_price_model.Petrol.id == petrol_id).first()


def page_petrol(db: Session, skip: int = 0, limit: int = 10):
    return db.query(petrol_price_model.Petrol).offset(skip).limit(limit).all()


def get_petrol_by_station_ids(db: Session, station_ids: list):
    return db.query(petrol_price_model.Petrol).filter(petrol_price_model.Petrol.gas_station_id.in_(station_ids)).all()


def get_petrol_by_station_id(db: Session, station_id: int):
    return db.query(petrol_price_model.Petrol).filter(petrol_price_model.Petrol.gas_station_id.eq(station_id)).all()


def create_petrol(db: Session, petrol: petrol_price_schema.PetrolCreateOrUpdate):
    db_petrol = petrol_price_model.Petrol(**petrol.dict())
    db.add(db_petrol)
    db.commit()
    db.refresh(db_petrol)
    return db_petrol


def update_petrol(db, cur_petrol, prev_petrol):
    if prev_petrol:
        for key, value in cur_petrol.dict().items():
            setattr(prev_petrol, key, value)
        db.commit()
        db.refresh(prev_petrol)
        return prev_petrol
    return None


def delete_petrol(db: Session, petrol_id: int):
    db_petrol = db.query(petrol_price_model.Petrol).filter(petrol_price_model.Petrol.id == petrol_id).first()
    if db_petrol:
        db.delete(db_petrol)
        db.commit()
        return db_petrol
    return None
