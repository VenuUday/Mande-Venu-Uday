import json
from data_processor import WeatherDataProcessor

# Load configuration
with open("../config/config.json") as f:
    config = json.load(f)

# Initialize WeatherDataProcessor
processor = WeatherDataProcessor(
    api_key=config["api_key"],
    cities=config["cities"],
    fetch_interval=config["fetch_interval"],
    alert_threshold=config["alert_threshold"]
)

# Start monitoring weather
if __name__ == "__main__":
    processor.start_processing()
