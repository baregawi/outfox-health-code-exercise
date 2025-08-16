import requests

from typing import Optional


def get_gps_coordinates(address: str) -> Optional[tuple]:
    """Fetch GPS coordinates for a given address using OpenStreetMap's Nominatim API."""

    # Replace spaces with '+' for URL encoding
    address = address.replace(' ', '+')

    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"
    response = requests.get(url, headers={'User-Agent': 'Foo bar'})
    json_response = response.json()

    if not json_response:
        return None

    lat = float(json_response[0]['lat'])
    long = float(json_response[0]['lon'])

    return lat, long