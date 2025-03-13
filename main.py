# main py dosyası
import multiprocessing
import time
from extract import run_flask
from load import save_weather_from_api
import requests

if __name__ == "__main__":
    flask_process = multiprocessing.Process(target=run_flask)
    flask_process.start()

    time.sleep(5)

    test_url = "http://127.0.0.1:5000/weather"
    try:
        response = requests.get(test_url)
        if response.status_code == 200:
            print("Flask API başarıyla çalışıyor!")
        else:
            print(f"Flask API Hata Kodu: {response.status_code}")
    except Exception as e:
        print("Flask API başlatılamadı:", e)
        flask_process.terminate()
        exit()

    save_weather_from_api()

    flask_process.terminate()