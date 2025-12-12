"""User agent rotation manager."""

import random
from fake_useragent import UserAgent
from typing import Optional


class UserAgentManager:
    """Manages user agent rotation."""

    def __init__(self, logger=None):
        """Initialize user agent manager.

        Args:
            logger: Logger instance
        """
        self.logger = logger
        self.ua = UserAgent()

        # Fallback user agents in case fake_useragent fails
        self.fallback_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
        ]

    def _log(self, level: str, message: str) -> None:
        """Log message if logger is available.

        Args:
            level: Log level (info, warning, error)
            message: Message to log
        """
        if self.logger:
            getattr(self.logger, level)(message)

    def get_random_user_agent(self) -> str:
        """Get a random user agent.

        Returns:
            Random user agent string
        """
        try:
            user_agent = self.ua.random
            self._log('info', "Generated random user agent")
            return user_agent
        except Exception as e:
            self._log('warning', f"Failed to get random user agent: {str(e)}, using fallback")
            return self.get_fallback_user_agent()

    def get_chrome_user_agent(self) -> str:
        """Get a Chrome user agent.

        Returns:
            Chrome user agent string
        """
        try:
            user_agent = self.ua.chrome
            self._log('info', "Generated Chrome user agent")
            return user_agent
        except Exception as e:
            self._log('warning', f"Failed to get Chrome user agent: {str(e)}, using fallback")
            return self.get_fallback_user_agent()

    def get_firefox_user_agent(self) -> str:
        """Get a Firefox user agent.

        Returns:
            Firefox user agent string
        """
        try:
            user_agent = self.ua.firefox
            self._log('info', "Generated Firefox user agent")
            return user_agent
        except Exception as e:
            self._log('warning', f"Failed to get Firefox user agent: {str(e)}, using fallback")
            return self.get_fallback_user_agent()

    def get_fallback_user_agent(self) -> str:
        """Get a fallback user agent from predefined list.

        Returns:
            Fallback user agent string
        """
        user_agent = random.choice(self.fallback_agents)
        self._log('info', "Using fallback user agent")
        return user_agent
