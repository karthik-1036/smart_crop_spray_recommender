import requests

def get_lat_lon(place):
    """
    Get latitude and longitude for a location using Open-Meteo Geocoding API.
    """
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={place}&count=1"
    res = requests.get(url)

    if res.status_code != 200:
        raise Exception("❌ Failed to fetch location coordinates")

    data = res.json()
    if "results" not in data or len(data["results"]) == 0:
        raise Exception("❌ Location not found")

    lat = data["results"][0]["latitude"]
    lon = data["results"][0]["longitude"]
    return lat, lon


def get_weather_data(lat, lon):
    """
    Get average temperature, humidity, wind speed and 2-day rainfall using Open-Meteo API.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
        f"&forecast_days=2&timezone=auto"
    )

    res = requests.get(url)
    if res.status_code != 200:
        raise Exception("❌ Failed to fetch weather data")

    data = res.json()

    # Extract the last 24 hours (Day 2 forecast)
    temp = data["hourly"]["temperature_2m"][-24:]
    humidity = data["hourly"]["relative_humidity_2m"][-24:]
    rainfall = data["hourly"]["precipitation"][-24:]
    wind = data["hourly"]["wind_speed_10m"][-24:]

    return {
        "temperature": round(sum(temp) / len(temp), 2),
        "humidity": round(sum(humidity) / len(humidity), 2),
        "rainfall_2d": round(sum(rainfall), 2),
        "wind_speed": round(sum(wind) / len(wind), 2),
    }
