"""Dependency checker for verifying required packages."""

import importlib
import subprocess
import sys
from typing import List, Tuple


class DependencyChecker:
    """Checks and installs required dependencies."""

    def __init__(self, logger=None):
        """Initialize dependency checker.

        Args:
            logger: Logger instance for logging messages
        """
        self.logger = logger

    def _log(self, level: str, message: str) -> None:
        """Log message if logger is available.

        Args:
            level: Log level (info, warning, error)
            message: Message to log
        """
        if self.logger:
            getattr(self.logger, level)(message)
        else:
            print(f"[{level.upper()}] {message}")

    def check_package(self, package_name: str) -> bool:
        """Check if a package is installed.

        Args:
            package_name: Name of the package to check

        Returns:
            True if package is installed, False otherwise
        """
        try:
            importlib.import_module(package_name)
            return True
        except ImportError:
            return False

    def check_dependencies(self, packages: List[str]) -> Tuple[List[str], List[str]]:
        """Check multiple dependencies.

        Args:
            packages: List of package names to check

        Returns:
            Tuple of (installed_packages, missing_packages)
        """
        installed = []
        missing = []

        for package in packages:
            if self.check_package(package):
                installed.append(package)
                self._log('info', f"✓ {package} is installed")
            else:
                missing.append(package)
                self._log('warning', f"✗ {package} is missing")

        return installed, missing

    def install_requirements(self, requirements_file: str = "requirements.txt") -> bool:
        """Install packages from requirements.txt.

        Args:
            requirements_file: Path to requirements file

        Returns:
            True if installation successful, False otherwise
        """
        try:
            self._log('info', f"Installing dependencies from {requirements_file}...")
            
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", requirements_file],
                capture_output=True,
                text=True,
                check=True
            )
            
            self._log('info', "Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self._log('error', f"Failed to install dependencies: {e.stderr}")
            return False
        except Exception as e:
            self._log('error', f"Error installing dependencies: {str(e)}")
            return False

    def check_all_dependencies(self) -> bool:
        """Check all required dependencies.

        Returns:
            True if all dependencies are met, False otherwise
        """
        required_packages = [
            'selenium',
            'undetected_chromedriver',
            'requests',
            'fake_useragent'
        ]

        self._log('info', "Checking dependencies...")
        installed, missing = self.check_dependencies(required_packages)

        if missing:
            self._log('warning', f"Missing packages: {', '.join(missing)}")
            return False
        
        self._log('info', "All dependencies are satisfied")
        return True
