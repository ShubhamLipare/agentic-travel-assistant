
import requests
from langchain_core.tools import tool

TIMEOUT = 100


@tool
def get_weather(city: str) -> dict:
    """Get the current weather for a city using Open-Meteo."""
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en"},
            timeout=TIMEOUT,
        )
        geo.raise_for_status()
        places = geo.json().get("results", [])

        if not places:
            return {"error": f"City not found: {city}"}

        place = places[0]
        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m,relative_humidity_2m,"
                           "apparent_temperature,wind_speed_10m",
            },
            timeout=TIMEOUT,
        )
        weather.raise_for_status()

        return {
            "city": place["name"],
            "country": place.get("country"),
            "weather": weather.json().get("current", {}),
        }
    except requests.RequestException as exc:
        return {"error": f"Weather API request failed: {exc}"}


@tool
def get_country_info(country: str) -> dict:
    """Get basic country information such as capital, region and population."""
    try:
        response = requests.get(
            f"https://restcountries.com/v3.1/name/{country}",
            params={"fields": "name,capital,region,population,languages,currencies"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        countries = response.json()

        if not countries:
            return {"error": f"Country not found: {country}"}

        data = countries[0]
        return {
            "name": data.get("name", {}).get("common"),
            "capital": data.get("capital", []),
            "region": data.get("region"),
            "population": data.get("population"),
            "languages": list(data.get("languages", {}).values()),
            "currencies": list(data.get("currencies", {}).keys()),
        }
    except requests.RequestException as exc:
        return {"error": f"Country API request failed: {exc}"}
