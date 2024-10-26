import time
from datetime import datetime
from alert_manager import AlertManager
from utilities.api_client import fetch_weather_data
from utilities.conversions import kelvin_to_celsius
from collections import defaultdict
import statistics

class WeatherDataProcessor:
    def __init__(self, api_key, cities, fetch_interval, alert_threshold):
        self.api_key = api_key
        self.cities = cities
        self.fetch_interval = fetch_interval
        self.alert_manager = AlertManager(alert_threshold)
        self.data_store = defaultdict(list)  # Stores weather data by city

    def process_data(self, city, data):
        temp = kelvin_to_celsius(data["main"]["temp"])
        weather_main = data["weather"][0]["main"]
        timestamp = datetime.utcfromtimestamp(data["dt"])

        self.data_store[city].append({
            "temp": temp,
            "weather_main": weather_main,
            "timestamp": timestamp
        })

    def calculate_daily_summary(self, city):
        day_data = [entry for entry in self.data_store[city]
                    if entry["timestamp"].date() == datetime.utcnow().date()]

        if day_data:
            avg_temp = statistics.mean(entry["temp"] for entry in day_data)
            max_temp = max(entry["temp"] for entry in day_data)
            min_temp = min(entry["temp"] for entry in day_data)
            dominant_weather = statistics.mode(entry["weather_main"] for entry in day_data)

            return {
                "city": city,
                "date": datetime.utcnow().date(),
                "avg_temp": avg_temp,
                "max_temp": max_temp,
                "min_temp": min_temp,
                "dominant_weather": dominant_weather
            }
        return None

    def start_processing(self):
        while True:
            for city in self.cities:
                data = fetch_weather_data(city, self.api_key)
                if data:
                    self.process_data(city, data)
                    self.alert_manager.check_alerts(city, self.data_store[city])

            time.sleep(self.fetch_interval)
