from datetime import datetime

import requests

api_weather = 'https://api.openweathermap.org/data/2.5/weather?'
api_geo = 'http://api.openweathermap.org/geo/1.0/direct?'
api_lat  = 'lat='
api_lon  = '&lon='
api_exclude = '&exclude='
api_units = '&units='
api_lang = '&lang='
api_key  = '&appid=25ed922d88ef42f527ce2f0b63a22c6a'
api_city = 'q='
api_limit = '&limit='

def get_weather_coord(lat, lon, exclude=None, units="metric", lang=None):
    url = (api_weather + api_lat + lat + api_lon + lon + api_key)
    if exclude is not None:
        url += api_exclude + exclude
    if units is not None:
        url += api_units + units
    if lang is not None:
        url += api_lang + lang

    response = requests.get(url)
    data = response.json()

    sunrise = str(datetime.fromtimestamp(int(data['sys']['sunrise'])))
    sunset = str(datetime.fromtimestamp(int(data['sys']['sunset'])))

    readable_data = {
        'city': data['name'],
        'temp': data['main']['temp'],
        'temp_min': data['main']['temp_min'],
        'temp_max': data['main']['temp_max'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
        'wind_direction': data['wind']['deg'],
        'clouds': data['clouds']['all'],
        'visibility': data['visibility'],
        'sunrise': sunrise,
        'sunset': sunset,
        'weather_description': data['weather'][0]['description']
    }

    return readable_data

def get_weather_city(city, limit="5"):
    url = api_geo + api_city + city + api_key + api_limit + limit
    response = requests.get(url)
    data = response.json()
    return data
