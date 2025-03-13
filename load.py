# load py dosyası
import psycopg
import requests
from datetime import datetime

# PostgreSQL bağlantı bilgileri
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "7991",
    "host": "localhost",
    "port": "5432"
}


# PostgreSQL bağlantısını açan ve tabloyu oluşturan fonksiyon
def init_db():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS weather_data (
                    time TIMESTAMP PRIMARY KEY,
                    temperature FLOAT,
                    wind_speed FLOAT
                )
            """)
            conn.commit()


# API’den veri alıp veritabanına kaydeden fonksiyon
def save_weather_from_api():
    url = "http://127.0.0.1:5000/weather"  # extract.py'deki API adresi
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()

        if "error" in weather_data:
            print("API Hatası:", weather_data["error"])
            return

        try:
            weather_time = datetime.strptime(weather_data['time'],
                                             "%Y-%m-%dT%H:%M")  # ISO formatını uygun hale getiriyoruz.
        except ValueError:
            print("Zaman formatı hatalı:", weather_data['time'])
            return

        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO weather_data (time, temperature, wind_speed)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (time) DO UPDATE SET
                        temperature = EXCLUDED.temperature,
                        wind_speed = EXCLUDED.wind_speed
                """, (weather_time, weather_data['temperature'], weather_data['wind_speed']))
                conn.commit()
        print("Veri kaydedildi:", weather_data)
    else:
        print("API'den veri çekme hatası:", response.status_code)


if __name__ == "__main__":
    init_db()  #  tablo yoksa oluştur
    save_weather_from_api()  #  al ve kaydet