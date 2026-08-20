# 🌤️ Weather Dashboard

A Python-based weather dashboard that fetches real-time weather data from OpenWeatherMap API with both CLI and web interfaces.

## Features

✅ **Real-time Weather Data**
- Current weather conditions
- 5-day forecast
- Multiple location support
- Search functionality

✅ **Temperature Units**
- Celsius (metric)
- Fahrenheit (imperial)

✅ **Interfaces**
- Command-line interface (CLI)
- Interactive web dashboard (Flask)

✅ **Data Points**
- Temperature and "feels like" temperature
- Humidity and pressure
- Wind speed and direction
- Cloud coverage
- Weather description

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/gerlieann0122/GitHub.git
cd GitHub
git checkout weather-dashboard
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get API Key
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key
4. Create `.env` file:
```bash
cp .env.example .env
```
5. Add your API key to `.env`:
```
OPENWEATHER_API_KEY=your_api_key_here
```

## Usage

### Command-Line Interface

```bash
python weather_dashboard.py
```

This will display:
- Current weather for London
- 5-day forecast for New York
- Weather for Paris by coordinates
- City search results

### Interactive Web Dashboard

```bash
python app.py
```

Then open your browser to:
```
http://localhost:5000
```

### Python API

```python
from weather_dashboard import WeatherDashboard

# Initialize
dashboard = WeatherDashboard()
dashboard.set_units("metric")  # or "imperial"

# Get current weather
weather = dashboard.get_current_weather("London")
print(dashboard.format_current_weather(weather))

# Get forecast
forecast = dashboard.get_forecast("London")
print(dashboard.format_forecast(forecast))

# Search cities
cities = dashboard.search_cities("New")
for city in cities:
    print(f"{city['name']}, {city['sys']['country']}")

# Get weather by coordinates
weather = dashboard.get_weather_by_coordinates(51.5074, -0.1278)  # London
print(dashboard.format_current_weather(weather))
```

## API Endpoints

When running the Flask app, these endpoints are available:

### Get Current Weather
```
GET /api/weather?city=London&units=metric
```

Response:
```json
{
  "success": true,
  "city": "London",
  "temperature": 15.2,
  "description": "partly cloudy",
  "humidity": 72,
  "pressure": 1013,
  "wind_speed": 4.5,
  "data": { ... }
}
```

### Get Forecast
```
GET /api/forecast?city=London&units=metric&days=5
```

### Search Cities
```
GET /api/search?q=New
```

### Get Weather by Coordinates
```
GET /api/coordinates?lat=51.5074&lon=-0.1278&units=metric
```

## Project Structure

```
.
├── weather_dashboard.py    # Main dashboard class
├── app.py                  # Flask web application
├── templates/
│   └── index.html          # Web UI (to be created)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Configuration

### Environment Variables

```env
# Required
OPENWEATHER_API_KEY=your_key_here

# Optional (for Flask)
FLASK_ENV=development
FLASK_DEBUG=True
```

## Examples

### Example 1: Get Weather for a City
```python
from weather_dashboard import WeatherDashboard

dashboard = WeatherDashboard()
dashboard.display_weather("Tokyo")
```

### Example 2: Compare Multiple Cities
```python
cities = ["New York", "London", "Tokyo", "Sydney"]
for city in cities:
    dashboard.display_weather(city)
```

### Example 3: Temperature Unit Conversion
```python
# Display in Celsius
dashboard.set_units("metric")
dashboard.display_weather("Berlin")

# Display in Fahrenheit
dashboard.set_units("imperial")
dashboard.display_weather("Berlin")
```

### Example 4: Check Weather Alerts
```python
weather = dashboard.get_current_weather("London")
temp = weather["main"]["temp"]

if temp < 0:
    print("❄️  Freezing conditions!")
elif temp > 30:
    print("🔥 High temperature alert!")
```

## Troubleshooting

### "OPENWEATHER_API_KEY not set"
- Add your API key to `.env` file
- Or set environment variable: `export OPENWEATHER_API_KEY=your_key`

### "Invalid API Key"
- Check if your API key is correct
- Ensure your OpenWeatherMap account is active
- Free tier has rate limits (60 calls/minute)

### "City Not Found"
- Try using the city search functionality
- Use coordinates instead: `dashboard.get_weather_by_coordinates(lat, lon)`

### "Connection Error"
- Check your internet connection
- Verify OpenWeatherMap API is accessible
- Try using a VPN if geographically restricted

## Performance Tips

✅ Cache API responses to reduce calls
✅ Use coordinates for faster lookups
✅ Batch requests for multiple cities
✅ Implement request throttling
✅ Store historical data for trends

## Future Enhancements

- 🌍 Interactive map view
- 📊 Historical weather charts
- 🔔 Weather alerts and notifications
- 📱 Mobile-responsive design
- 🌙 Dark mode
- 🗺️ Multiple location tracking
- 💾 Database integration
- 🔄 Real-time updates with WebSockets

## API Rate Limits

OpenWeatherMap Free Tier:
- 60 calls/minute
- 1,000,000 calls/month

## License

MIT License - Feel free to use and modify

## Resources

- [OpenWeatherMap API Documentation](https://openweathermap.org/api)
- [OpenWeatherMap Free Tier](https://openweathermap.org/weather)
- [Weather Icons](https://openweathermap.org/weather-conditions)
- [Flask Documentation](https://flask.palletsprojects.com/)

## Support

For issues or questions:
1. Check the [OpenWeatherMap FAQ](https://openweathermap.org/faq)
2. Review the [API Documentation](https://openweathermap.org/api)
3. Open an issue on GitHub

---

**Made with ❤️ using Python and OpenWeatherMap API**
