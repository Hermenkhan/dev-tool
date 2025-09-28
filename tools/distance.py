import requests
from math import radians, sin, cos, sqrt, atan2

API_KEY = "52420d959f5749cfbd67a5258d590195"
BASE_URL = "https://api.opencagedata.com/geocode/v1/json"


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def geocode(location):
    url = f"{BASE_URL}?q={location}&key={API_KEY}"
    resp = requests.get(url)
    data = resp.json()
    coords = data["results"][0]["geometry"]
    return coords["lat"], coords["lng"]


def get_distance(location1: str, location2: str, raw: bool = False):
    """
    Calculate distance between two locations.
    """
    try:
        lat1, lon1 = geocode(location1)
        lat2, lon2 = geocode(location2)

        distance = haversine(radians(lat1), radians(lon1), radians(lat2), radians(lon2))

        if raw:
            coords = [{"lat": lat1, "lon": lon1}, {"lat": lat2, "lon": lon2}]
            return f"{distance:.2f} km", coords

        return f"The distance between {location1} and {location2} is {distance:.2f} km."
    except Exception as e:
        return f"Error calculating distance: {e}"
