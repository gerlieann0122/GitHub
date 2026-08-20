"""
Weather Dashboard - Fetches real-time weather data from OpenWeatherMap API

Features:
- Current weather conditions
- 5-day forecast
- Multiple location search
- Temperature unit conversion (Celsius/Fahrenheit)
- Weather alerts
"""

import os
import json
import requests
from typing import Optional, Dict, List
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# OpenWeatherMap API Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"


class WeatherDashboard:
    """Main weather dashboard class for fetching and displaying weather data."""

    def __init__(self, api_key: str = OPENWEATHER_API_KEY):
        """Initialize weather dashboard with API key."""
        self.api_key = api_key
        self.base_url = OPENWEATHER_BASE_URL
        self.units = "metric"  # Default to Celsius

    def set_units(self, units: str = "metric") -> None:
        """Set temperature units (metric=Celsius, imperial=Fahrenheit)."""
        if units in ["metric", "imperial"]:
            self.units = units
        else:
            raise ValueError("Units must be 'metric' or 'imperial'")

    def get_current_weather(self, city: str) -> Optional[Dict]:
        """
        Fetch current weather for a specific city.

        Args:
            city: City name

        Returns:
            Dictionary containing current weather data
        """
        if not self.api_key:
            print("⚠️  OPENWEATHER_API_KEY not set. Using mock data.")
            return self._get_mock_current_weather(city)

        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": self.units,
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching weather: {e}")
            return None

    def get_forecast(self, city: str, days: int = 5) -> Optional[Dict]:
        """
        Fetch weather forecast for a city.

        Args:
            city: City name
            days: Number of days to forecast (1-5)

        Returns:
            Dictionary containing forecast data
        """
        if not self.api_key:
            print("⚠️  OPENWEATHER_API_KEY not set. Using mock data.")
            return self._get_mock_forecast(city)

        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": self.units,
                "cnt": days * 8,  # 8 forecasts per day (3-hour intervals)
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching forecast: {e}")
            return None

    def get_weather_by_coordinates(
        self, latitude: float, longitude: float
    ) -> Optional[Dict]:
        """
        Fetch current weather by geographic coordinates.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            Dictionary containing weather data
        """
        if not self.api_key:
            print("⚠️  OPENWEATHER_API_KEY not set. Using mock data.")
            return self._get_mock_current_weather(f"({latitude}, {longitude})")

        try:
            url = f"{self.base_url}/weather"
            params = {
                "lat": latitude,
                "lon": longitude,
                "appid": self.api_key,
                "units": self.units,
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching weather: {e}")
            return None

    def format_current_weather(self, weather_data: Dict) -> str:
        """
        Format current weather data for display.

        Args:
            weather_data: Weather data dictionary from API

        Returns:
            Formatted string for display
        """
        if not weather_data:
            return "No weather data available"

        try:
            city = weather_data.get("name", "Unknown")
            country = weather_data.get("sys", {}).get("country", "")
            temp = weather_data.get("main", {}).get("temp", "N/A")
            feels_like = weather_data.get("main", {}).get("feels_like", "N/A")
            humidity = weather_data.get("main", {}).get("humidity", "N/A")
            pressure = weather_data.get("main", {}).get("pressure", "N/A")
            description = weather_data.get("weather", [{}])[0].get(
                "description", "N/A"
            )
            wind_speed = weather_data.get("wind", {}).get("speed", "N/A")
            clouds = weather_data.get("clouds", {}).get("all", "N/A")

            unit = "°C" if self.units == "metric" else "°F"
            wind_unit = "m/s" if self.units == "metric" else "mph"

            return f"""
╔════════════════════════════════════════╗
║  Weather Dashboard - {city}, {country}
╠════════════════════════════════════════╣
║ Temperature:      {temp}{unit} (feels like {feels_like}{unit})
║ Condition:        {description.capitalize()}
║ Humidity:         {humidity}%
║ Pressure:         {pressure} hPa
║ Wind Speed:       {wind_speed} {wind_unit}
║ Cloud Coverage:   {clouds}%
╚════════════════════════════════════════╝
            """
        except (KeyError, TypeError) as e:
            return f"Error formatting weather data: {e}"

    def format_forecast(self, forecast_data: Dict) -> str:
        """
        Format forecast data for display.

        Args:
            forecast_data: Forecast data dictionary from API

        Returns:
            Formatted string for display
        """
        if not forecast_data:
            return "No forecast data available"

        try:
            city = forecast_data.get("city", {}).get("name", "Unknown")
            forecasts = forecast_data.get("list", [])

            output = f"\n5-Day Forecast for {city}\n"
            output += "=" * 60 + "\n"

            for i, forecast in enumerate(forecasts[::8]):  # Every 8th entry (24 hours)
                if i >= 5:
                    break
                dt = datetime.fromtimestamp(forecast["dt"])
                temp = forecast["main"]["temp"]
                description = forecast["weather"][0]["description"]
                humidity = forecast["main"]["humidity"]

                unit = "°C" if self.units == "metric" else "°F"
                output += f"{dt.strftime('%A, %Y-%m-%d')} | Temp: {temp}{unit} | {description.capitalize()} | Humidity: {humidity}%\n"

            return output
        except (KeyError, TypeError) as e:
            return f"Error formatting forecast: {e}"

    def display_weather(self, city: str) -> None:
        """
        Fetch and display current weather for a city.

        Args:
            city: City name
        """
        print(f"\n🌤️  Fetching weather for {city}...")
        weather = self.get_current_weather(city)
        print(self.format_current_weather(weather))

    def display_forecast(self, city: str) -> None:
        """
        Fetch and display forecast for a city.

        Args:
            city: City name
        """
        print(f"\n📅 Fetching forecast for {city}...")
        forecast = self.get_forecast(city)
        print(self.format_forecast(forecast))

    def search_cities(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search for cities matching a query.

        Args:
            query: City name or partial name
            limit: Maximum number of results

        Returns:
            List of matching cities
        """
        if not self.api_key:
            print("⚠️  OPENWEATHER_API_KEY not set.")
            return []

        try:
            url = f"{self.base_url}/find"
            params = {"q": query, "appid": self.api_key, "cnt": limit}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get("list", [])
        except requests.exceptions.RequestException as e:
            print(f"❌ Error searching cities: {e}")
            return []

    def _get_mock_current_weather(self, city: str) -> Dict:
        """Return mock weather data for testing."""
        return {
            "name": city,
            "sys": {"country": "XX"},
            "main": {
                "temp": 22,
                "feels_like": 21,
                "humidity": 65,
                "pressure": 1013,
            },
            "weather": [{"description": "partly cloudy"}],
            "wind": {"speed": 3.5},
            "clouds": {"all": 40},
        }

    def _get_mock_forecast(self, city: str) -> Dict:
        """Return mock forecast data for testing."""
        return {
            "city": {"name": city},
            "list": [
                {
                    "dt": int(datetime.now().timestamp()),
                    "main": {"temp": 22, "humidity": 65},
                    "weather": [{"description": "partly cloudy"}],
                }
            ],
        }


def main():
    """Main function to demonstrate weather dashboard."""
    print("\n" + "=" * 60)
    print("🌍 WEATHER DASHBOARD")
    print("=" * 60)

    # Initialize dashboard
    dashboard = WeatherDashboard()
    dashboard.set_units("metric")  # Use Celsius

    # Example 1: Display current weather
    print("\n📍 Example 1: Current Weather")
    dashboard.display_weather("London")

    # Example 2: Display forecast
    print("\n📍 Example 2: Weather Forecast")
    dashboard.display_forecast("New York")

    # Example 3: Weather by coordinates
    print("\n📍 Example 3: Weather by Coordinates")
    print("Fetching weather for Paris (48.8566°N, 2.3522°E)...")
    weather = dashboard.get_weather_by_coordinates(48.8566, 2.3522)
    print(dashboard.format_current_weather(weather))

    # Example 4: Search cities
    print("\n📍 Example 4: Search Cities")
    cities = dashboard.search_cities("San")
    if cities:
        print("Found cities matching 'San':")
        for city in cities[:5]:
            print(f"  - {city['name']}, {city['sys']['country']}")


if __name__ == "__main__":
    main()
