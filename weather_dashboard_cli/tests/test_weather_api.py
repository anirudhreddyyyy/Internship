import unittest
from unittest.mock import patch
from weather_api import get_current_weather

class TestWeatherAPI(unittest.TestCase):

    @patch("weather_api.requests.get")
    def test_get_current_weather(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "name": "London",
            "main": {"temp": 20},
            "weather": [{"description": "clear sky"}]
        }

        data = get_current_weather("London")
        self.assertEqual(data["name"], "London")
        self.assertEqual(data["main"]["temp"], 20)

if __name__ == "__main__":
    unittest.main()