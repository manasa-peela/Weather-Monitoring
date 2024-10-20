import requests
from config import API_KEY, BASE_URL
from datetime import datetime


def get_weather_data(city_id):
    params = {'id': city_id, 'appid': API_KEY}
    response = requests.get(BASE_URL, params=params,timeout=10)
    response.raise_for_status()
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.json()}")
        return None


def kelvin_to_celsius(kelvin_temp):
    return kelvin_temp - 273.15


def parse_weather_data(weather_data):
    if 'main' not in weather_data:
        print(f"Error in response: {weather_data}")  # Log the error
        return None  # Skip further processing if data is invalid

    temp_kelvin = weather_data['main']['temp']
    temp_celsius = kelvin_to_celsius(temp_kelvin)
    # feels_like_celsius = kelvin_to_celsius(weather_data['main']['feels_like'])
    weather_condition = weather_data['weather'][0]['main']
    timestamp = datetime.now()
    
    return {
        'temp': temp_celsius,
        'weather_condition': weather_condition,
        'timestamp': timestamp
    }

