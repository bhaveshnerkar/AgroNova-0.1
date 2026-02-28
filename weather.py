import requests
import os

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

def get_weather_by_location(location: str) -> dict:
    """
    Fetch real weather data from OpenWeatherMap API.
    Returns temperature, humidity, rainfall estimate.
    """
    if not OPENWEATHER_API_KEY:
        # Return demo data if no API key (for testing)
        return get_demo_weather(location)

    try:
        # Get current weather
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location + ",IN",  # Prioritize India
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 404:
            # Try without ,IN suffix
            params["q"] = location
            response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return {"success": False, "error": "Location not found"}

        data = response.json()

        # Get rainfall from forecast (annual estimate)
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast"
        forecast_resp = requests.get(forecast_url, params=params, timeout=10)
        
        # Estimate annual rainfall from current data
        rain_1h = data.get("rain", {}).get("1h", 0)
        estimated_annual_rain = rain_1h * 8760  # rough estimate
        
        # Better: use known regional averages based on coordinates
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
        estimated_annual_rain = estimate_annual_rainfall(lat, lon)

        return {
            "success": True,
            "location": data["name"],
            "country": data["sys"]["country"],
            "temperature": round(data["main"]["temp"], 1),
            "humidity": round(data["main"]["humidity"], 1),
            "description": data["weather"][0]["description"],
            "rainfall_annual_mm": estimated_annual_rain,
            "coordinates": {
                "lat": lat,
                "lon": lon
            }
        }

    except requests.exceptions.ConnectionError:
        return get_demo_weather(location)
    except Exception as e:
        return {"success": False, "error": str(e)}


def estimate_annual_rainfall(lat: float, lon: float) -> float:
    """
    Estimate annual rainfall based on India's rainfall zones by coordinates.
    These are approximate regional averages.
    """
    # India rainfall zones (approximate)
    # High rainfall: Northeast, Western Ghats, Coastal areas
    # Medium: Central India
    # Low: Rajasthan, Gujarat dry areas

    # Northeast India (Assam, Meghalaya etc.)
    if lat > 22 and lon > 88 and lon < 97:
        return 2000

    # Western Ghats & Kerala coast
    if lat < 15 and lon < 78:
        return 2500

    # Coastal Karnataka/Goa
    if lat >= 14 and lat <= 18 and lon < 75:
        return 1800

    # Rajasthan (dry)
    if lat > 24 and lon < 75:
        return 300

    # Gujarat (semi-dry)
    if lat > 20 and lat < 24 and lon < 74:
        return 600

    # Maharashtra (Vidarbha, Marathwada)
    if lat >= 17 and lat <= 22 and lon >= 74 and lon <= 80:
        return 900

    # Central India (MP, Chhattisgarh)
    if lat >= 20 and lat <= 26 and lon >= 76 and lon <= 84:
        return 1100

    # Punjab, Haryana
    if lat > 28 and lon >= 74 and lon <= 78:
        return 700

    # UP, Bihar
    if lat >= 24 and lat <= 30 and lon >= 78 and lon <= 88:
        return 900

    # Tamil Nadu
    if lat < 13:
        return 900

    # Default: average India
    return 900


def get_demo_weather(location: str) -> dict:
    """
    Return demo weather data when no API key is available.
    Used for testing/demo purposes.
    """
    # Some known Indian cities with approximate data
    known_cities = {
        "mumbai": {"temp": 29, "humidity": 75, "rain": 2200},
        "pune": {"temp": 26, "humidity": 60, "rain": 750},
        "delhi": {"temp": 25, "humidity": 55, "rain": 700},
        "nashik": {"temp": 24, "humidity": 58, "rain": 680},
        "nagpur": {"temp": 28, "humidity": 60, "rain": 1100},
        "aurangabad": {"temp": 25, "humidity": 55, "rain": 720},
        "kolhapur": {"temp": 25, "humidity": 72, "rain": 1400},
        "bangalore": {"temp": 24, "humidity": 65, "rain": 970},
        "chennai": {"temp": 30, "humidity": 75, "rain": 1400},
        "hyderabad": {"temp": 27, "humidity": 62, "rain": 800},
        "jaipur": {"temp": 28, "humidity": 45, "rain": 550},
        "lucknow": {"temp": 26, "humidity": 62, "rain": 900},
        "patna": {"temp": 27, "humidity": 68, "rain": 1100},
        "bhopal": {"temp": 26, "humidity": 58, "rain": 1150},
        "indore": {"temp": 26, "humidity": 55, "rain": 900},
        "surat": {"temp": 29, "humidity": 70, "rain": 1100},
        "ahmedabad": {"temp": 29, "humidity": 55, "rain": 780},
        "amravati": {"temp": 27, "humidity": 58, "rain": 950},
        "solapur": {"temp": 28, "humidity": 50, "rain": 560},
        "latur": {"temp": 27, "humidity": 52, "rain": 620},
    }

    loc_lower = location.lower().strip()
    city_data = None

    for city, data in known_cities.items():
        if city in loc_lower or loc_lower in city:
            city_data = data
            break

    if city_data:
        return {
            "success": True,
            "location": location.title(),
            "country": "IN",
            "temperature": city_data["temp"],
            "humidity": city_data["humidity"],
            "description": "partly cloudy",
            "rainfall_annual_mm": city_data["rain"],
            "demo_mode": True,
            "note": "Demo data — add OPENWEATHER_API_KEY in .env for real data"
        }
    else:
        # Generic India average
        return {
            "success": True,
            "location": location.title(),
            "country": "IN",
            "temperature": 26,
            "humidity": 62,
            "description": "partly cloudy",
            "rainfall_annual_mm": 900,
            "demo_mode": True,
            "note": "Demo data — add OPENWEATHER_API_KEY in .env for real data"
        }
