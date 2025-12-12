"""YouTube video viewer automation."""

import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from typing import Optional


class YouTubeViewer:
    """Handles YouTube video viewing automation."""

    def __init__(self, driver, logger=None, delays: Optional[dict] = None):
        """Initialize YouTube viewer.

        Args:
            driver: Selenium WebDriver instance
            logger: Logger instance
            delays: Dictionary of delay configurations
        """
        self.driver = driver
        self.logger = logger
        self.delays = delays or {
            'min_watch_time': 30,
            'max_watch_time': 120,
            'min_delay_between_videos': 5,
            'max_delay_between_videos': 15
        }

    def _log(self, level: str, message: str) -> None:
        """Log message if logger is available.

        Args:
            level: Log level (info, warning, error)
            message: Message to log
        """
        if self.logger:
            getattr(self.logger, level)(message)

    def _random_delay(self, min_seconds: int, max_seconds: int) -> None:
        """Sleep for a random duration.

        Args:
            min_seconds: Minimum seconds to sleep
            max_seconds: Maximum seconds to sleep
        """
        delay = random.uniform(min_seconds, max_seconds)
        self._log('info', f"Waiting {delay:.2f} seconds...")
        time.sleep(delay)

    def watch_video(self, url: str, watch_time: Optional[int] = None) -> bool:
        """Watch a YouTube video.

        Args:
            url: YouTube video URL
            watch_time: Time to watch in seconds (optional, uses config if not provided)

        Returns:
            True if video was watched successfully, False otherwise
        """
        try:
            self._log('info', f"Navigating to: {url}")
            self.driver.get(url)

            # Wait for video player to load
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.ID, "movie_player"))
                )
                self._log('info', "Video player loaded")
            except TimeoutException:
                self._log('warning', "Video player not found, continuing anyway")

            # Handle consent/cookie dialog if present
            self._handle_consent_dialog()

            # Click play button if video is paused
            self._ensure_video_playing()

            # Determine watch time
            if watch_time is None:
                watch_time = random.randint(
                    self.delays.get('min_watch_time', 30),
                    self.delays.get('max_watch_time', 120)
                )

            self._log('info', f"Watching video for {watch_time} seconds...")

            # Watch video with periodic checks
            elapsed = 0
            check_interval = 10
            while elapsed < watch_time:
                time.sleep(min(check_interval, watch_time - elapsed))
                elapsed += check_interval

                # Verify page is still active
                try:
                    self.driver.current_url
                except WebDriverException as e:
                    self._log('error', f"Browser connection lost: {str(e)}")
                    return False

            self._log('info', f"Successfully watched video: {url}")
            return True

        except WebDriverException as e:
            self._log('error', f"WebDriver error while watching video: {str(e)}")
            return False
        except Exception as e:
            self._log('error', f"Unexpected error while watching video: {str(e)}")
            return False

    def _handle_consent_dialog(self) -> None:
        """Handle YouTube consent/cookie dialog if present."""
        try:
            # Try to find and click "Accept all" button
            accept_buttons = [
                "//button[@aria-label='Accept all']",
                "//button[contains(text(), 'Accept all')]",
                "//button[contains(text(), 'Agree')]",
                "//ytd-button-renderer[@id='accept-button']"
            ]

            for xpath in accept_buttons:
                try:
                    button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    button.click()
                    self._log('info', "Accepted consent dialog")
                    time.sleep(2)
                    return
                except TimeoutException:
                    continue

        except Exception as e:
            self._log('debug', f"No consent dialog found or error handling it: {str(e)}")

    def _ensure_video_playing(self) -> None:
        """Ensure video is playing."""
        try:
            # Wait a moment for auto-play
            time.sleep(3)

            # Try to click play button if video is paused
            play_button = self.driver.find_element(By.CLASS_NAME, "ytp-play-button")
            if play_button.get_attribute("aria-label") and "Play" in play_button.get_attribute("aria-label"):
                play_button.click()
                self._log('info', "Clicked play button")
                time.sleep(2)
        except Exception as e:
            self._log('debug', f"Video auto-playing or play button not found: {str(e)}")

    def delay_between_videos(self) -> None:
        """Add delay between watching videos."""
        min_delay = self.delays.get('min_delay_between_videos', 5)
        max_delay = self.delays.get('max_delay_between_videos', 15)
        self._random_delay(min_delay, max_delay)
