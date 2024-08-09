from crud import petrol_station_crud, petrol_price_crud
from requsts.google_map_request import get_direction_points
from schemas.bounding_box import BoundingBox
import math


def get_station_by_route(db, src_lat, src_lon, dest_lat, dest_lon):
    # TODO: increase the efficiency on querying petrol station
    points = get_direction_points(src_lat, src_lon, dest_lat, dest_lon)
    boxes = computer_bounding_boxes(points, 500)
    petrol_station_box_list = []
    petrol_station_dict = {}
    # petrol_station_crud.get_petrol_station_by_bounding_boxes_paginated(db, boxes, 50)
    for bounding in boxes:
        per_petrol_station_list = petrol_station_crud.get_petrol_station_by_bounding_box(db, bounding)
        petrol_station_box_list.extend(per_petrol_station_list)
    for petrol_station in petrol_station_box_list:
        petrol_station_dict[petrol_station.id] = petrol_station

    # filter_petrol_station_ids = list(petrol_station_dict.keys())
    #
    # # get the petrol by station id
    # petrol_list = petrol_price_crud.get_petrol_by_station_ids(db, filter_petrol_station_ids)
    #
    # petrol_dict = {}
    #
    # for petrol in petrol_list:
    #     if petrol_dict.get(petrol.gas_station_id):
    #         petrol_dict[petrol.gas_station_id].append(petrol)
    #     else:
    #         petrol_dict[petrol.gas_station_id] = [petrol]
    #
    # for station_id in petrol_dict.keys():
    #     petrol_station_dict[station_id].petrol_list = petrol_dict[station_id]

    filter_petrol_station = list(petrol_station_dict.values())
    return filter_petrol_station


def computer_bounding_boxes(points, range_meters):
    boxes = []
    # computing the bounding boxes based on the range
    for point in points:
        boxes.append(get_bounding_box_by_range(point[0], point[1], range_meters))
    return boxes


def get_bounding_box_by_range(lat, lng, range_meters):
    earth_radius = 6371000  # Earth's radius in meters

    # Convert range from meters to degrees
    range_in_degrees = (range_meters / earth_radius) * (180 / math.pi)

    # Calculate bounding box
    lat_min = lat - range_in_degrees
    lat_max = lat + range_in_degrees

    # Longitude degrees vary with latitude, so we need to calculate this separately
    lng_range_in_degrees = (
            range_meters / (earth_radius * math.cos(math.radians(lat))) * (180 / math.pi)
    )
    lng_min = lng - lng_range_in_degrees
    lng_max = lng + lng_range_in_degrees

    return BoundingBox(sw_lat=lat_min, ne_lat=lat_max, sw_lng=lng_min, ne_lng=lng_max)
