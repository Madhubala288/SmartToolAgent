import httpx
def get_weather(latitude: float, longitude: float) -> dict:
    """
    Get current weather information using Open-Meteo.
    Args:
        latitude: Location latitude.
        longitude: Location longitude.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "wind_speed_10m"
        ),
    }
    response = httpx.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return {
        "latitude": latitude,
        "longitude": longitude,
        "temperature_c": data["current"]["temperature_2m"],
        "humidity_percent": data["current"]["relative_humidity_2m"],
        "apparent_temperature_c": data["current"]["apparent_temperature"],
        "wind_speed_kmh": data["current"]["wind_speed_10m"],
    }