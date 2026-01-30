import pytest
from unittest.mock import patch
import builtins

from Mini_Project_2 import display_weather, display_forecast, main


# ----------------------------
# Mock data
# ----------------------------

MOCK_WEATHER = {
    "name": "Chennai",
    "main": {
        "temp": 30,
        "humidity": 65
    },
    "weather": [
        {"description": "clear sky"}
    ]
}

MOCK_FORECAST = {
    "list": [
        {
            "dt_txt": "2026-01-30 09:00:00",
            "main": {"temp": 31},
            "weather": [{"description": "sunny"}]
        }
    ] * 8
}


# ----------------------------
# Display function tests
# ----------------------------

def test_display_weather(capsys):
    display_weather(MOCK_WEATHER)

    captured = capsys.readouterr()
    assert "Chennai" in captured.out
    assert "30°C" in captured.out
    assert "clear sky" in captured.out
    assert "65%" in captured.out


def test_display_forecast(capsys):
    display_forecast(MOCK_FORECAST)

    captured = capsys.readouterr()
    assert "Forecast" in captured.out
    assert "2026-01-30" in captured.out
    assert "31°C" in captured.out
    assert "sunny" in captured.out


# ----------------------------
# Main flow test (happy path)
# ----------------------------

@patch("Mini_Project_2.get_current_weather")
@patch("Mini_Project_2.get_forecast")
@patch("Mini_Project_2.save_history")
@patch.object(builtins, "input", lambda _: "Chennai")
def test_main_success(mock_save, mock_forecast, mock_weather):
    mock_weather.return_value = MOCK_WEATHER
    mock_forecast.return_value = MOCK_FORECAST

    main()

    mock_weather.assert_called_once_with("Chennai")
    mock_forecast.assert_called_once_with("Chennai")
    mock_save.assert_called_once_with("Chennai", MOCK_WEATHER)


# ----------------------------
# API failure test
# ----------------------------

@patch("Mini_Project_2.get_current_weather")
@patch.object(builtins, "input", lambda _: "InvalidCity")
def test_main_api_failure(mock_weather, capsys):
    mock_weather.side_effect = Exception("City not found")

    main()

    captured = capsys.readouterr()
    assert "Error" in captured.out
    assert "City not found" in captured.out


# ----------------------------
# Forecast failure test
# ----------------------------

@patch("Mini_Project_2.get_current_weather")
@patch("Mini_Project_2.get_forecast")
@patch.object(builtins, "input", lambda _: "Delhi")
def test_main_forecast_failure(mock_forecast, mock_weather, capsys):
    mock_weather.return_value = MOCK_WEATHER
    mock_forecast.side_effect = Exception("Forecast API failed")

    main()

    captured = capsys.readouterr()
    assert "Error" in captured.out
    assert "Forecast API failed" in captured.out
