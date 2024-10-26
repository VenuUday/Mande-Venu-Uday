import unittest
from alert_manager import AlertManager

class TestAlertManager(unittest.TestCase):
    def test_check_alerts(self):
        alert_manager = AlertManager(threshold=30)
        data = [{"temp": 32}]
        
        with self.assertLogs(level="INFO") as log:
            alert_manager.check_alerts("Delhi", data)
            self.assertIn("ALERT: Delhi temperature exceeded 30°C", log.output[0])

if __name__ == "__main__":
    unittest.main()
