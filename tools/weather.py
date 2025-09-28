import requests

API_KEY = "049048adef5f0ac4aa3012b93db79b78"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str, raw: bool = False):
    """
    Fetches current weather for a given city.

    Args:
        city (str): City name
        raw (bool): If True, return JSON dict. Else return formatted string.

    Returns:
        dict | str
    """
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if raw:
            return data

        city_name = data["name"]
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        return (
            f"Weather in {city_name}:\n"
            f"Temperature: {temp}°C\n"
            f"Condition: {desc.capitalize()}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind} m/s"
        )
    except requests.exceptions.HTTPError:
        return "City not found. Please check the city name."
    except Exception as e:
        return f"Error: {e}"
