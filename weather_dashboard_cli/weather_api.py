
import requests
from config import BASE_URL, FORECAST_URL
from dotenv import load_dotenv
import os

load_dotenv()


def get_current_weather(city):
    params = {
        "q": city,
        "appid": os.getenv("API_KEY"),
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def get_forecast(city):
    params = {
        "q": city,
        "appid": os.getenv("API_KEY"),
        "units": "metric"
    }
    response = requests.get(FORECAST_URL, params=params)
    response.raise_for_status()
    return response.json()
