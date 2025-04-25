# weather_app.py
from flask import Flask, request, jsonify
import time
import random

app = Flask(__name__)

@app.route('/')
def home():
    return """
        <h2>Welcome to Simple Weather API</h2>
        <p>Try <code>/weather?city=London</code></p>
    """

@app.route('/weather')
def get_weather():
    city = request.args.get('city', 'Unknown')
    
    # Simulate delay to mimic processing load
    time.sleep(random.uniform(1, 2))  
    
    # Dummy weather response
    data = {
        "city": city,
        "temperature": f"{random.randint(20, 35)}°C",
        "status": random.choice(["Sunny", "Cloudy", "Rainy"])
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
