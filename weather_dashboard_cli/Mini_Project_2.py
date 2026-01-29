from weather_api import get_current_weather, get_forecast
from storage import save_history

def display_weather(data):
    print("\nCurrent Weather")
    print("----------------")
    print(f"City: {data['name']}")
    print(f"Temperature: {data['main']['temp']}°C")
    print(f"Condition: {data['weather'][0]['description']}")
    print(f"Humidity: {data['main']['humidity']}%")

def display_forecast(forecast):
    print("\nForecast (Next 24 hrs)")
    print("----------------------")
    for item in forecast["list"][:8]:
        print(f"{item['dt_txt']} | {item['main']['temp']}°C | {item['weather'][0]['description']}")

def main():
    city = input("Enter city name: ")

    try:
        weather = get_current_weather(city)
        forecast = get_forecast(city)

        display_weather(weather)
        display_forecast(forecast)

        save_history(city, weather)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
