"""Integration tests for YouTube Viewer Bot."""

import unittest
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(Path(__file__).parent.parent, 'src'))

from modules.config_manager import ConfigManager
from modules.logger import Logger
from modules.dependency_checker import DependencyChecker
from modules.proxy_manager import ProxyManager
from modules.user_agent_manager import UserAgentManager


class TestIntegration(unittest.TestCase):
    """Integration test cases."""

    def setUp(self):
        """Set up test fixtures."""
        self.config_manager = ConfigManager()
        self.logger = Logger(log_level="ERROR")  # Reduce noise in tests

    def test_config_manager_integration(self):
        """Test ConfigManager loads and provides config."""
        self.assertIsNotNone(self.config_manager.config)
        self.assertIsInstance(self.config_manager.get_youtube_urls(), list)
        self.assertIsInstance(self.config_manager.get_delays(), dict)

    def test_dependency_checker_integration(self):
        """Test DependencyChecker verifies packages."""
        checker = DependencyChecker(self.logger)
        result = checker.check_all_dependencies()
        self.assertTrue(result, "All dependencies should be installed")

    def test_proxy_manager_integration(self):
        """Test ProxyManager with empty proxy list."""
        proxies = self.config_manager.get_proxies()
        manager = ProxyManager(proxies, self.logger)
        self.assertFalse(manager.has_proxies())
        self.assertIsNone(manager.get_random_proxy())

    def test_proxy_manager_with_proxies(self):
        """Test ProxyManager with proxy list."""
        test_proxies = ["proxy1:8080", "proxy2:3128"]
        manager = ProxyManager(test_proxies, self.logger)
        self.assertTrue(manager.has_proxies())
        self.assertEqual(manager.get_proxy_count(), 2)
        proxy = manager.get_random_proxy()
        self.assertIn(proxy, test_proxies)

    def test_user_agent_manager_integration(self):
        """Test UserAgentManager generates user agents."""
        manager = UserAgentManager(self.logger)
        
        # Test Chrome user agent
        ua_chrome = manager.get_chrome_user_agent()
        self.assertIsInstance(ua_chrome, str)
        self.assertTrue(len(ua_chrome) > 0)
        
        # Test random user agent
        ua_random = manager.get_random_user_agent()
        self.assertIsInstance(ua_random, str)
        self.assertTrue(len(ua_random) > 0)

    def test_config_and_managers_integration(self):
        """Test integration between config and managers."""
        # Load config
        rotation_config = self.config_manager.get_rotation_config()
        self.assertIsInstance(rotation_config, dict)
        
        # Test proxy manager with config
        proxies = self.config_manager.get_proxies()
        proxy_manager = ProxyManager(proxies, self.logger)
        
        if rotation_config.get('rotate_proxy') and proxy_manager.has_proxies():
            proxy = proxy_manager.get_random_proxy()
            self.assertIsNotNone(proxy)
        
        # Test user agent manager
        if rotation_config.get('rotate_user_agent'):
            ua_manager = UserAgentManager(self.logger)
            ua = ua_manager.get_chrome_user_agent()
            self.assertIsNotNone(ua)

    def test_delays_configuration(self):
        """Test delays are properly configured."""
        delays = self.config_manager.get_delays()
        self.assertIn('min_watch_time', delays)
        self.assertIn('max_watch_time', delays)
        self.assertGreater(delays['max_watch_time'], delays['min_watch_time'])


if __name__ == '__main__':
    unittest.main()
