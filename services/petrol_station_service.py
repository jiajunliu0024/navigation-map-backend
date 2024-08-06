from crud import petrol_station_crud
from database import SessionLocal


def get_station_by_bounding_boxes(db, boxes):
    petrol_station_box_list = []
    for bounding in boxes:
        petrol_station_box_list.add(petrol_station_crud.get_petrol_station_by_bounding_box(db, bounding));

    return petrol_station_box_list
