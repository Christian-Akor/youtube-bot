"""Main YouTube Bot application."""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from modules.config_manager import ConfigManager
from modules.logger import Logger
from modules.dependency_checker import DependencyChecker
from modules.driver_manager import DriverManager
from modules.proxy_manager import ProxyManager
from modules.user_agent_manager import UserAgentManager
from modules.youtube_viewer import YouTubeViewer


class YouTubeBot:
    """Main YouTube Bot application."""

    def __init__(self, config_path: str = None):
        """Initialize YouTube Bot.

        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config_manager = ConfigManager(config_path)
        
        # Setup logger
        log_level = self.config_manager.get_log_level()
        self.logger = Logger(log_level=log_level)
        
        self.logger.info("=" * 60)
        self.logger.info("YouTube Viewer Bot - Starting")
        self.logger.info("=" * 60)

        # Initialize managers
        self.proxy_manager = ProxyManager(
            self.config_manager.get_proxies(),
            self.logger
        )
        self.user_agent_manager = UserAgentManager(self.logger)
        self.driver_manager = DriverManager(
            self.logger,
            self.config_manager.get_browser_config()
        )
        
        self.driver = None
        self.youtube_viewer = None

    def check_dependencies(self) -> bool:
        """Check if all dependencies are installed.

        Returns:
            True if all dependencies are met, False otherwise
        """
        self.logger.info("Checking dependencies...")
        dependency_checker = DependencyChecker(self.logger)
        return dependency_checker.check_all_dependencies()

    def setup_driver(self) -> bool:
        """Setup Chrome WebDriver with appropriate configuration.

        Returns:
            True if driver setup successful, False otherwise
        """
        try:
            # Get rotation config
            rotation_config = self.config_manager.get_rotation_config()
            
            # Get user agent if rotation is enabled
            user_agent = None
            if rotation_config.get('rotate_user_agent', False):
                user_agent = self.user_agent_manager.get_chrome_user_agent()
            
            # Get proxy if rotation is enabled and proxies are available
            proxy = None
            if rotation_config.get('rotate_proxy', False) and self.proxy_manager.has_proxies():
                proxy = self.proxy_manager.get_random_proxy()
            
            # Create driver
            self.driver = self.driver_manager.create_driver(
                user_agent=user_agent,
                proxy=proxy
            )
            
            # Initialize YouTube viewer
            self.youtube_viewer = YouTubeViewer(
                self.driver,
                self.logger,
                self.config_manager.get_delays()
            )
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to setup driver: {str(e)}", exc_info=True)
            return False

    def run(self) -> None:
        """Run the YouTube Bot."""
        try:
            # Check dependencies
            if not self.check_dependencies():
                self.logger.error("Dependency check failed. Please install requirements.")
                return

            # Get YouTube URLs
            youtube_urls = self.config_manager.get_youtube_urls()
            if not youtube_urls:
                self.logger.error("No YouTube URLs configured")
                return

            self.logger.info(f"Found {len(youtube_urls)} video(s) to watch")

            # Setup driver
            if not self.setup_driver():
                self.logger.error("Failed to setup driver")
                return

            # Watch videos
            max_retries = self.config_manager.get_max_retries()
            
            for idx, url in enumerate(youtube_urls, 1):
                self.logger.info(f"\n{'=' * 60}")
                self.logger.info(f"Processing video {idx}/{len(youtube_urls)}")
                self.logger.info(f"{'=' * 60}")
                
                success = False
                for attempt in range(1, max_retries + 1):
                    self.logger.info(f"Attempt {attempt}/{max_retries}")
                    
                    if self.youtube_viewer.watch_video(url):
                        success = True
                        break
                    else:
                        self.logger.warning(f"Failed to watch video (attempt {attempt}/{max_retries})")
                        if attempt < max_retries:
                            self.logger.info("Retrying...")
                
                if not success:
                    self.logger.error(f"Failed to watch video after {max_retries} attempts: {url}")
                
                # Add delay between videos if not the last video
                if idx < len(youtube_urls):
                    self.youtube_viewer.delay_between_videos()

            self.logger.info("\n" + "=" * 60)
            self.logger.info("YouTube Bot - Completed")
            self.logger.info("=" * 60)

        except KeyboardInterrupt:
            self.logger.info("\nBot stopped by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        finally:
            # Cleanup
            self.cleanup()

    def cleanup(self) -> None:
        """Cleanup resources."""
        self.logger.info("Cleaning up resources...")
        if self.driver_manager:
            self.driver_manager.quit_driver()
        self.logger.info("Cleanup completed")


def main():
    """Main entry point."""
    bot = YouTubeBot()
    bot.run()


if __name__ == "__main__":
    main()
