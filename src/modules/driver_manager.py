"""ChromeDriver manager for automatic updates and configuration."""

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from typing import Optional, Dict, Any


class DriverManager:
    """Manages Chrome WebDriver with automatic updates."""

    def __init__(self, logger=None, config: Optional[Dict[str, Any]] = None):
        """Initialize driver manager.

        Args:
            logger: Logger instance
            config: Browser configuration dictionary
        """
        self.logger = logger
        self.config = config or {}
        self.driver = None

    def _log(self, level: str, message: str) -> None:
        """Log message if logger is available.

        Args:
            level: Log level (info, warning, error)
            message: Message to log
        """
        if self.logger:
            getattr(self.logger, level)(message)

    def create_driver(self, user_agent: Optional[str] = None, 
                     proxy: Optional[str] = None) -> uc.Chrome:
        """Create and configure Chrome WebDriver.

        Args:
            user_agent: Custom user agent string
            proxy: Proxy address (format: host:port or user:pass@host:port)

        Returns:
            Configured Chrome WebDriver instance
        """
        self._log('info', "Creating Chrome WebDriver...")

        options = uc.ChromeOptions()

        # Headless mode
        if self.config.get('headless', False):
            options.add_argument('--headless=new')
            self._log('info', "Running in headless mode")

        # Window size
        window_size = self.config.get('window_size', '1920,1080')
        options.add_argument(f'--window-size={window_size}')

        # Performance optimizations
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')

        # Disable images for faster loading
        if self.config.get('disable_images', False):
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)
            self._log('info', "Image loading disabled")

        # Custom user agent
        if user_agent:
            options.add_argument(f'--user-agent={user_agent}')
            self._log('info', f"Using custom user agent")

        # Proxy configuration
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
            self._log('info', f"Using proxy: {proxy}")

        # Additional options for stealth
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        try:
            # Create driver with undetected-chromedriver
            # This automatically handles ChromeDriver updates
            self.driver = uc.Chrome(options=options, use_subprocess=True)
            
            # Set page load timeout
            self.driver.set_page_load_timeout(60)
            
            self._log('info', "Chrome WebDriver created successfully")
            return self.driver
        except Exception as e:
            self._log('error', f"Failed to create WebDriver: {str(e)}")
            raise

    def quit_driver(self) -> None:
        """Safely quit the WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
                self._log('info', "WebDriver closed successfully")
            except Exception as e:
                self._log('error', f"Error closing WebDriver: {str(e)}")
            finally:
                self.driver = None

    def get_driver(self) -> Optional[uc.Chrome]:
        """Get current driver instance.

        Returns:
            Current driver instance or None
        """
        return self.driver
