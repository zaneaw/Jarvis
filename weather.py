import os
import requests

from dotenv import load_dotenv
load_dotenv()

def weather(city):
    api_key = os.getenv('WEATHER_API_KEY')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}"
    response = requests.get(url)
    x = response.json()

    if x['cod'] != '404':
        y = x['main']
        z = x['weather']
        curr_temp = y['temp']
        curr_humidity = y['humidity']
        return(f"The current temperature is {int(curr_temp)} fahrenheit and the humidity is {curr_humidity} percent.")