from crud import petrol_station_crud, petrol_price_crud
from crud.petrol_station_crud import get_petrol_station_id
from requsts.google_map_request import get_direction_points, get_direction_info, get_direction_info_with_waypoints
from schemas.bounding_box import BoundingBox
import math
import logging
from typing import List
from sqlalchemy.orm import Session
from utils.exceptions import InvalidCoordinatesException

logger = logging.getLogger(__name__)


def get_servo_by_map(db, sw_lat, sw_lng, ne_lat, ne_lng):
    box = BoundingBox(sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)
    return petrol_station_crud.get_petrol_station_by_bounding_box(db, box)


def get_by_pass_info(db, src_lat, src_lon, dest_lat, dest_lon, station_id, petrol_type):
    origin_direction = get_direction_info(src_lat, src_lon, dest_lat, dest_lon)
    # get the current by pass direction
    src_point = str(src_lat) + "," + str(src_lon)
    des_point = str(dest_lat) + "," + str(dest_lon)

    petrol_station = get_petrol_station_id(db, station_id)
    way_point = str(petrol_station.location_y) + "," + str(petrol_station.location_x)

    by_pass_direction = get_direction_info_with_waypoints(src_point, des_point, way_point)
    for petrol in petrol_station.petrol_list:
        if petrol_type == petrol.type:
            petrol_price = petrol.amount
            break
    origin_km = get_km_from_direction(origin_direction)
    by_pass_km = get_km_from_direction(by_pass_direction)

    different_km = by_pass_km - origin_km
    cost = different_km * petrol_price / 100
    by_pass_info = {"distance": round(different_km, 3), "cost": round(cost, 3), "price": petrol_price}
    return by_pass_info


def get_km_from_direction(directions_data):
    total_distance = 0
    for route in directions_data['routes']:
        for leg in route['legs']:
            total_distance += leg['distance']['value']  # Distance in meters
        # Convert meters to kilometers
    total_distance_km = total_distance / 1000
    return total_distance_km


def get_station_by_route(db: Session, src_lat: float, src_lng: float, 
                        des_lat: float, des_lng: float) -> List:
    try:
        logger.info(f"Fetching stations for route from ({src_lat},{src_lng}) to ({des_lat},{des_lng})")
        # Validate coordinates
        if not (-90 <= src_lat <= 90) or not (-90 <= des_lat <= 90):
            raise InvalidCoordinatesException()
            
        # TODO: increase the efficiency on querying petrol station
        points = get_direction_points(src_lat, src_lng, des_lat, des_lng)
        boxes = computer_bounding_boxes(points, 500)
        petrol_station_box_list = []
        petrol_station_dict = {}
        # petrol_station_crud.get_petrol_station_by_bounding_boxes_paginated(db, boxes, 50)
        for bounding in boxes:
            per_petrol_station_list = petrol_station_crud.get_petrol_station_by_bounding_box(db, bounding)
            petrol_station_box_list.extend(per_petrol_station_list)
        for petrol_station in petrol_station_box_list:
            petrol_station_dict[petrol_station.id] = petrol_station

        filter_petrol_station = list(petrol_station_dict.values())
        return filter_petrol_station

    except Exception as e:
        logger.error(f"Error fetching stations: {str(e)}")
        raise


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
