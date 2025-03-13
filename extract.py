# extract py dosyası
import requests
from flask import Flask, jsonify

app = Flask(__name__)

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 39.7767,
        "longitude": 30.5206,
        "current_weather": "true"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'current_weather' in data:
            weather_data = {
                "time": data['current_weather']['time'],
                "temperature": data['current_weather']['temperature'],
                "wind_speed": data['current_weather']['windspeed']
            }
            return weather_data
        else:
            return {"error": "API response format is incorrect"}
    else:
        return {"error": f"Failed to fetch data: {response.status_code}"}

@app.route('/weather', methods=['GET'])
def weather_api():
    return jsonify(get_weather())

def run_flask():
    print("Flask API going...")
    app.run(debug=True, use_reloader=False, port=5000)

if __name__ == '__main__':
    run_flask()