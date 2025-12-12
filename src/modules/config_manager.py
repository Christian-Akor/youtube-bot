"""Configuration manager for loading and validating config."""

import json
import os
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manages application configuration."""

    def __init__(self, config_path: str = None):
        """Initialize configuration manager.

        Args:
            config_path: Path to config file. Defaults to config/config.json
        """
        if config_path is None:
            base_dir = Path(__file__).parent.parent.parent
            config_path = os.path.join(base_dir, "config", "config.json")
        
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file.

        Returns:
            Configuration dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        self.validate_config(config)
        return config

    def validate_config(self, config: Dict[str, Any]) -> None:
        """Validate configuration structure.

        Args:
            config: Configuration dictionary to validate

        Raises:
            ValueError: If configuration is invalid
        """
        required_keys = ['youtube_urls', 'delays', 'browser', 'rotation']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required config key: {key}")

        if not isinstance(config['youtube_urls'], list) or not config['youtube_urls']:
            raise ValueError("youtube_urls must be a non-empty list")

        if not isinstance(config['delays'], dict):
            raise ValueError("delays must be a dictionary")

        required_delays = ['min_watch_time', 'max_watch_time']
        for key in required_delays:
            if key not in config['delays']:
                raise ValueError(f"Missing required delay key: {key}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.

        Args:
            key: Configuration key
            default: Default value if key doesn't exist

        Returns:
            Configuration value
        """
        return self.config.get(key, default)

    def get_youtube_urls(self) -> list:
        """Get list of YouTube URLs.

        Returns:
            List of YouTube URLs
        """
        return self.config.get('youtube_urls', [])

    def get_proxies(self) -> list:
        """Get list of proxies.

        Returns:
            List of proxy addresses
        """
        return self.config.get('proxies', [])

    def get_delays(self) -> Dict[str, int]:
        """Get delay configuration.

        Returns:
            Dictionary of delay settings
        """
        return self.config.get('delays', {})

    def get_browser_config(self) -> Dict[str, Any]:
        """Get browser configuration.

        Returns:
            Dictionary of browser settings
        """
        return self.config.get('browser', {})

    def get_rotation_config(self) -> Dict[str, bool]:
        """Get rotation configuration.

        Returns:
            Dictionary of rotation settings
        """
        return self.config.get('rotation', {})

    def get_max_retries(self) -> int:
        """Get max retries setting.

        Returns:
            Maximum number of retries
        """
        return self.config.get('max_retries', 3)

    def get_log_level(self) -> str:
        """Get log level setting.

        Returns:
            Log level string
        """
        return self.config.get('log_level', 'INFO')
