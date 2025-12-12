"""Tests for ConfigManager module."""

import unittest
import json
import tempfile
import os
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, os.path.join(Path(__file__).parent.parent, 'src'))

from modules.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_config = {
            "youtube_urls": ["https://www.youtube.com/watch?v=test"],
            "proxies": [],
            "delays": {
                "min_watch_time": 30,
                "max_watch_time": 120,
                "min_delay_between_videos": 5,
                "max_delay_between_videos": 15
            },
            "browser": {
                "headless": False,
                "window_size": "1920,1080"
            },
            "rotation": {
                "rotate_user_agent": True,
                "rotate_proxy": False
            },
            "max_retries": 3,
            "log_level": "INFO"
        }

    def test_load_valid_config(self):
        """Test loading a valid configuration."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.test_config, f)
            temp_path = f.name

        try:
            config_manager = ConfigManager(temp_path)
            self.assertIsNotNone(config_manager.config)
            self.assertEqual(config_manager.get_youtube_urls(), self.test_config['youtube_urls'])
        finally:
            os.unlink(temp_path)

    def test_get_youtube_urls(self):
        """Test getting YouTube URLs."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.test_config, f)
            temp_path = f.name

        try:
            config_manager = ConfigManager(temp_path)
            urls = config_manager.get_youtube_urls()
            self.assertEqual(len(urls), 1)
            self.assertIn("youtube.com", urls[0])
        finally:
            os.unlink(temp_path)

    def test_validate_config_missing_key(self):
        """Test validation with missing required key."""
        invalid_config = {"youtube_urls": []}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(invalid_config, f)
            temp_path = f.name

        try:
            with self.assertRaises(ValueError):
                ConfigManager(temp_path)
        finally:
            os.unlink(temp_path)

    def test_get_delays(self):
        """Test getting delay configuration."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.test_config, f)
            temp_path = f.name

        try:
            config_manager = ConfigManager(temp_path)
            delays = config_manager.get_delays()
            self.assertEqual(delays['min_watch_time'], 30)
            self.assertEqual(delays['max_watch_time'], 120)
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
