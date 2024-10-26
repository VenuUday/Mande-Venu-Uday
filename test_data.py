import unittest
from data_processor import WeatherDataProcessor
from unittest.mock import patch, MagicMock
from datetime import datetime

class TestWeatherDataProcessor(unittest.TestCase):
    @patch('utilities.api_client.fetch_weather_data')
    def test_process_data(self, mock_fetch):
        mock_fetch.return_value = {
            "main": {"temp": 300},
            "weather": [{"main": "Clear"}],
            "dt": datetime.utcnow().timestamp()
        }

        processor = WeatherDataProcessor(api_key="dummy", cities=["Delhi"], fetch_interval=10, alert_threshold=35)
        processor.process_data("Delhi", mock_fetch.return_value)
        
        self.assertIn("Delhi", processor.data_store)
        self.assertEqual(len(processor.data_store["Delhi"]), 1)

    def test_calculate_daily_summary(self):
        processor = WeatherDataProcessor(api_key="dummy", cities=["Delhi"], fetch_interval=10, alert_threshold=35)
        sample_data = [
            {"temp": 30, "weather_main": "Clear", "timestamp": datetime.utcnow()},
            {"temp": 32, "weather_main": "Clouds", "timestamp": datetime.utcnow()},
            {"temp": 28, "weather_main": "Clear", "timestamp": datetime.utcnow()}
        ]
        processor.data_store["Delhi"].extend(sample_data)
        summary = processor.calculate_daily_summary("Delhi")

        self.assertAlmostEqual(summary["avg_temp"], 30, places=1)
        self.assertEqual(summary["dominant_weather"], "Clear")

if __name__ == "__main__":
    unittest.main()
