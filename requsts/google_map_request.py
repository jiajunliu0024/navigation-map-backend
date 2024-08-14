import requests
from fastapi import HTTPException
import httpx
import polyline

# Load API key from environment variable
GOOGLE_API_KEY = "AIzaSyA6d7pIq9TszfM0M6pIosMT1flSKr5o8oM"
GOOGLE_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"


def get_direction_points(start_lat: float, start_lng: float, end_lat: float, end_lng: float):
    data = get_direction_info(start_lat, start_lng, end_lat, end_lng)
    points = extract_overview_path(data)
    return points


def get_direction_info(start_lat: float, start_lng: float, end_lat: float, end_lng: float):
    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="API key is not set")

    with httpx.Client() as client:
        # Construct the request URL with latitude and longitude
        url = f"{GOOGLE_DIRECTIONS_URL}?origin={start_lat},{start_lng}&destination={end_lat},{end_lng}&key={GOOGLE_API_KEY}"

        # Make the request to Google Maps Directions API
        response = client.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch directions")


def get_direction_info_with_waypoints(origin, destination, waypoint):
    # Base URL for Google Maps Directions API
    base_url = "https://maps.googleapis.com/maps/api/directions/json"

    # Parameters for the API request
    params = {
        'origin': origin,
        'destination': destination,
        'waypoints': waypoint,
        'key': GOOGLE_API_KEY,
        'mode': 'driving',  # You can change this to 'walking', 'bicycling', or 'transit'
        'optimize': 'true'  # Optional: Optimize the waypoints order
    }
    # Make the request to the Google Maps Directions API
    response = requests.get(base_url, params=params)

    # Check for successful response
    if response.status_code == 200:
        directions_data = response.json()
        return directions_data
    else:
        return {"error": f"Failed to retrieve data: {response.status_code}"}


def extract_overview_path(data):
    try:
        # Extract overview polyline from the data
        overview_polyline = data.get('routes', [{}])[0].get('overview_polyline', {}).get('points')
        if not overview_polyline:
            raise HTTPException(status_code=404, detail="Overview polyline not found")

        # Decode the polyline
        overview_path = polyline.decode(overview_polyline)

        return overview_path
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Key error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
