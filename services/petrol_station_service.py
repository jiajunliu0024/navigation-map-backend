from crud import petrol_station_crud
from requsts.google_map_request import get_direction_points
import math


def get_station_by_route(db, src_lat, src_lon, dest_lat, dest_lon):
    points = get_direction_points(src_lat, src_lon, dest_lat, dest_lon)
    boxes = computer_bounding_boxes(points, 2000)
    petrol_station_box_list = []
    for bounding in boxes:
        petrol_station_box_list.add(petrol_station_crud.get_petrol_statzion_by_bounding_box(db, bounding));
    return petrol_station_box_list


def computer_bounding_boxes(points,range_meters):
    boxes = []
    # computing the bounding boxes based on the range
    for point in points:
        boxes.add(get_bounding_box_by_range(point[0], point[1], range_meters))
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

    return {
        'sw_lat': lat_min,
        'ne_lat': lat_max,
        'sw_lng': lng_min,
        'ne_lng': lng_max,
    }
