
import json
from config import HISTORY_FILE
from datetime import datetime

def save_history(city, weather_data):
    record = {
        "city": city,
        "temperature": weather_data["main"]["temp"],
        "condition": weather_data["weather"][0]["description"],
        "time": datetime.now().isoformat()
    }

    try:
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append(record)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)
