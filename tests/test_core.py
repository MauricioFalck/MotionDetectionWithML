from core import config
import os
import unittest


class TestCore(unittest.TestCase):
    def test_create_config_file(self):
        if os.path.exists(".\\config\\configuration.json"):
            os.remove(".\\config\\configuration.json")
        config.parse_config_json()
        self.assertEqual(os.path.exists(".\\config\\configuration.json"), True)

    def test_read_config_file(self):
        config_data = config.parse_config_json()
        self.assertEqual(config_data["display_video"], False)
