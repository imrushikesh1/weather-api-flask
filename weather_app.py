from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/weather')
def get_weather():
    city = request.args.get('city', '').strip()
    if not city:
        return render_template("error.html", message="Please enter a city name.")

    # 1. Geocode
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_res = requests.get(geo_url, params={"name": city, "count": 1}).json()
    if "results" not in geo_res or not geo_res["results"]:
        return render_template("error.html", message=f"City “{city}” not found.")

    loc = geo_res["results"][0]
    lat, lon = loc["latitude"], loc["longitude"]

    # 2. Current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
    }
    weather_res = requests.get(weather_url, params=params).json()
    cw = weather_res.get("current_weather", {})

    data = {
        "city": city.title(),
        "temperature": f"{cw.get('temperature', 'N/A')}°C",
        # map weathercode to description (simple)
        "status": {
            0: "Clear",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            61: "Rain",
            80: "Rain showers",
            95: "Thunderstorm"
        }.get(cw.get("weathercode"), "Unknown")
    }

    return render_template("weather.html", data=data)

if __name__ == "__main__":
    # use port 5000 to avoid sudo
    app.run(host="0.0.0.0", port=8000)
