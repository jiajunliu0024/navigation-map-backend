from fastapi import HTTPException
import httpx
import polyline

# Load API key from environment variable
GOOGLE_API_KEY = "AIzaSyA6d7pIq9TszfM0M6pIosMT1flSKr5o8oM"
GOOGLE_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"


def get_direction_points(start_lat: float, start_lng: float, end_lat: float, end_lng: float):
    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="API key is not set")

    with httpx.Client() as client:
        # Construct the request URL with latitude and longitude
        url = f"{GOOGLE_DIRECTIONS_URL}?origin={start_lat},{start_lng}&destination={end_lat},{end_lng}&key={GOOGLE_API_KEY}"

        # Make the request to Google Maps Directions API
        response = client.get(url)

        if response.status_code == 200:
            data = response.json()
            points = extract_overview_path(data)

            return points
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch directions")


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
