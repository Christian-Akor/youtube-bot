"""Proxy rotation manager."""

import random
from typing import Optional, List


class ProxyManager:
    """Manages proxy rotation."""

    def __init__(self, proxies: List[str], logger=None):
        """Initialize proxy manager.

        Args:
            proxies: List of proxy addresses
            logger: Logger instance
        """
        self.proxies = proxies
        self.logger = logger
        self.current_index = 0

    def _log(self, level: str, message: str) -> None:
        """Log message if logger is available.

        Args:
            level: Log level (info, warning, error)
            message: Message to log
        """
        if self.logger:
            getattr(self.logger, level)(message)

    def get_random_proxy(self) -> Optional[str]:
        """Get a random proxy from the list.

        Returns:
            Random proxy address or None if no proxies available
        """
        if not self.proxies:
            self._log('warning', "No proxies available")
            return None

        proxy = random.choice(self.proxies)
        self._log('info', f"Selected random proxy: {proxy}")
        return proxy

    def get_next_proxy(self) -> Optional[str]:
        """Get next proxy in rotation.

        Returns:
            Next proxy address or None if no proxies available
        """
        if not self.proxies:
            self._log('warning', "No proxies available")
            return None

        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        self._log('info', f"Selected proxy (rotation): {proxy}")
        return proxy

    def has_proxies(self) -> bool:
        """Check if proxies are available.

        Returns:
            True if proxies are available, False otherwise
        """
        return len(self.proxies) > 0

    def get_proxy_count(self) -> int:
        """Get number of available proxies.

        Returns:
            Number of proxies
        """
        return len(self.proxies)

    def validate_proxy_format(self, proxy: str) -> bool:
        """Validate proxy format.

        Args:
            proxy: Proxy string to validate

        Returns:
            True if format is valid, False otherwise
        """
        # Basic validation for proxy format
        # Supports: host:port or user:pass@host:port
        if not proxy or ':' not in proxy:
            return False
        return True
