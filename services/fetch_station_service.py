import logging

from fastapi import Depends
from sqlalchemy.orm import Session

from crud import petrol_station_crud
import uuid

from crud import petrol_price_crud
from database import SessionLocal
from schemas.petrol_station_schema import PetrolStationCreateOrUpdate
from schemas.petrol_price_schema import PetrolCreateOrUpdate
from models.petrol_station_model import PetrolStation
from models.petrol_price_model import Petrol


def get_petrol_station(db: Session, station_id: int):
    return db.query(PetrolStation).filter(PetrolStation.id == station_id).first()


def get_petrol_price_by_station_id_and_type(db, station_id, petrol_type):
    return db.query(Petrol).filter(Petrol.gas_station_id == station_id).filter(Petrol.type == petrol_type).first()


def update_petrol_and_petrol_station_data(petrol_spy_json):
    db = SessionLocal()
    try:
        petrol_station_list = petrol_spy_json['message']['list']
        petrol_station_index = 0
        for station in petrol_station_list:
            petrol_station = init_petrol_station_with_data(station)
            if get_petrol_station(db, petrol_station.id):
                petrol_station_crud.update_petrol_station(db, petrol_station.id, petrol_station)
                print("update petrol station", petrol_station_index)
            else:
                petrol_station_crud.create_petrol_station(db, petrol_station)
                print("create petrol station", petrol_station_index)
            insert_petrol_prices_data(db, station['prices'], station['id'])
            petrol_station_index += 1
    except Exception as e:
        print(e)


def insert_petrol_prices_data(db, prices, station_id):
    price_list = list(prices.values())
    petrol_index = 0
    for price in price_list:
        cur_petrol = init_petrol_with_data(price, station_id)
        prev_petrol = get_petrol_price_by_station_id_and_type(db, price.get('stationId'), price.get('type'))
        if prev_petrol:
            petrol_price_crud.update_petrol(db, cur_petrol, prev_petrol)
            print("update petrol station", petrol_index)
        else:
            petrol_price_crud.create_petrol(db, cur_petrol)
            print("create petrol station", petrol_index)
        petrol_index += 1

def init_petrol_station_with_data(station):
    petrol_station = PetrolStationCreateOrUpdate(
        id=station['id'],
        name=station['name'],
        brand=station['brand'],
        state=station['state'],
        suburb=station['suburb'],
        address=station['address'],
        postCode=station['postCode'],
        country=station['country'],
        phone=station.get('phone', 'none'),
        location_x=station['location']['x'],
        location_y=station['location']['y'],
        petrol_list=[],
        eft_ops=1 if station.get('eftops', 'False') == 'True' else 0,
        truck_park=1 if station.get('truckpark', 'False') == 'True' else 0,
        restrooms=1 if station.get('restrooms', 'False') == 'True' else 0,
        accessible=1 if station.get('accessible', 'False') == 'True' else 0,
        open24=1 if station.get('open24', 'False') == 'True' else 0,
    )
    return petrol_station


def init_petrol_with_data(price, station_id):
    price_id = price.get(id, str(uuid.uuid4()).replace('-', ''))
    petrol = PetrolCreateOrUpdate(id=price_id,
                                  gas_station_id=station_id,
                                  type=price['type'],
                                  updated=price['updated'],
                                  amount=price['amount'],
                                  )
    return petrol
