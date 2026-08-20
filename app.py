"""
Flask Web Application - Interactive Weather Dashboard

Provides a web interface for the weather dashboard.
Run with: python app.py
"""

from flask import Flask, render_template, request, jsonify
from weather_dashboard import WeatherDashboard
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Initialize weather dashboard
dashboard = WeatherDashboard()


@app.route("/")
def index():
    """Render main dashboard page."""
    return render_template("index.html")


@app.route("/api/weather", methods=["GET"])
def get_weather():
    """API endpoint to get current weather."""
    city = request.args.get("city", "London")
    units = request.args.get("units", "metric")

    dashboard.set_units(units)
    weather = dashboard.get_current_weather(city)

    if weather:
        return jsonify(
            {
                "success": True,
                "data": weather,
                "city": weather.get("name"),
                "temperature": weather["main"]["temp"],
                "description": weather["weather"][0]["description"],
                "humidity": weather["main"]["humidity"],
                "pressure": weather["main"]["pressure"],
                "wind_speed": weather["wind"]["speed"],
            }
        )
    else:
        return jsonify({"success": False, "error": "Failed to fetch weather"}), 400


@app.route("/api/forecast", methods=["GET"])
def get_forecast():
    """API endpoint to get weather forecast."""
    city = request.args.get("city", "London")
    units = request.args.get("units", "metric")
    days = request.args.get("days", 5, type=int)

    dashboard.set_units(units)
    forecast = dashboard.get_forecast(city, days)

    if forecast:
        return jsonify({"success": True, "data": forecast})
    else:
        return jsonify({"success": False, "error": "Failed to fetch forecast"}), 400


@app.route("/api/search", methods=["GET"])
def search_cities():
    """API endpoint to search cities."""
    query = request.args.get("q", "")
    if not query:
        return jsonify({"success": False, "error": "Query required"}), 400

    cities = dashboard.search_cities(query)
    if cities:
        return jsonify({"success": True, "data": cities})
    else:
        return jsonify({"success": False, "error": "No cities found"}), 404


@app.route("/api/coordinates", methods=["GET"])
def get_by_coordinates():
    """API endpoint to get weather by coordinates."""
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
        units = request.args.get("units", "metric")

        dashboard.set_units(units)
        weather = dashboard.get_weather_by_coordinates(lat, lon)

        if weather:
            return jsonify({"success": True, "data": weather})
        else:
            return (
                jsonify({"success": False, "error": "Failed to fetch weather"}),
                400,
            )
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "Invalid coordinates"}), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
