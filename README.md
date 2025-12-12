# YouTube Viewer Bot

A production-ready YouTube automation tool built with Python 3.12, Selenium, and undetected-chromedriver. This bot can automatically watch YouTube videos with features like proxy rotation, user-agent rotation, and detailed logging.

## Features

- ✅ **Python 3.12 Compatible** - Fully compatible with the latest Python version
- ✅ **Selenium + Undetected ChromeDriver** - Automated browser control with anti-detection
- ✅ **Modular Architecture** - Clean, maintainable code structure
- ✅ **Auto Dependency Checking** - Automatically verifies required packages
- ✅ **ChromeDriver Auto-Updates** - Automatic ChromeDriver version management
- ✅ **YouTube Watch Automation** - Automated video viewing with realistic behavior
- ✅ **Proxy Rotation** - Support for rotating proxies
- ✅ **User-Agent Rotation** - Random user-agent generation
- ✅ **Smart Delays** - Configurable random delays to mimic human behavior
- ✅ **Error Handling** - Comprehensive error handling and retry logic
- ✅ **Detailed Logging** - Timestamped logs for monitoring and debugging
- ✅ **Configuration File** - Easy-to-edit JSON configuration
- ✅ **Virtual Environment** - Isolated Python environment
- ✅ **Cross-Platform** - Works on Linux, macOS, and Windows

## Project Structure

```
youtube-bot/
├── config/
│   └── config.json          # Configuration file
├── logs/                     # Log files (auto-generated)
├── src/
│   ├── __init__.py
│   ├── youtube_bot.py       # Main bot application
│   └── modules/
│       ├── __init__.py
│       ├── config_manager.py       # Configuration management
│       ├── logger.py               # Logging system
│       ├── dependency_checker.py  # Dependency verification
│       ├── driver_manager.py      # WebDriver management
│       ├── proxy_manager.py       # Proxy rotation
│       ├── user_agent_manager.py  # User-agent rotation
│       └── youtube_viewer.py      # YouTube automation
├── tests/                    # Test files
├── .gitignore
├── requirements.txt          # Python dependencies
├── setup_venv.sh            # Linux/macOS setup script
├── setup_venv.bat           # Windows setup script
├── run.py                   # Main run script
└── README.md
```

## Requirements

- Python 3.12 or higher
- Google Chrome browser installed
- Internet connection

## Installation

### Linux/macOS

1. Clone the repository:
```bash
git clone https://github.com/Christian-Akor/youtube-bot.git
cd youtube-bot
```

2. Run the setup script:
```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

3. Activate the virtual environment:
```bash
source venv/bin/activate
```

### Windows

1. Clone the repository:
```cmd
git clone https://github.com/Christian-Akor/youtube-bot.git
cd youtube-bot
```

2. Run the setup script:
```cmd
setup_venv.bat
```

3. Activate the virtual environment:
```cmd
venv\Scripts\activate.bat
```

### Manual Installation

If you prefer to install manually:

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit `config/config.json` to customize the bot behavior:

```json
{
  "youtube_urls": [
    "https://www.youtube.com/watch?v=VIDEO_ID"
  ],
  "proxies": [],
  "delays": {
    "min_watch_time": 30,
    "max_watch_time": 120,
    "min_delay_between_videos": 5,
    "max_delay_between_videos": 15
  },
  "browser": {
    "headless": false,
    "window_size": "1920,1080",
    "disable_images": false
  },
  "rotation": {
    "rotate_user_agent": true,
    "rotate_proxy": true
  },
  "max_retries": 3,
  "log_level": "INFO"
}
```

### Configuration Options

- **youtube_urls**: List of YouTube video URLs to watch
- **proxies**: List of proxies (format: `host:port` or `user:pass@host:port`)
- **delays**: Time delays in seconds
  - `min_watch_time`: Minimum time to watch each video
  - `max_watch_time`: Maximum time to watch each video
  - `min_delay_between_videos`: Minimum delay between videos
  - `max_delay_between_videos`: Maximum delay between videos
- **browser**: Browser configuration
  - `headless`: Run in headless mode (true/false)
  - `window_size`: Browser window size
  - `disable_images`: Disable image loading for faster performance
- **rotation**: Rotation settings
  - `rotate_user_agent`: Enable user-agent rotation
  - `rotate_proxy`: Enable proxy rotation
- **max_retries**: Maximum retry attempts for failed videos
- **log_level**: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## Usage

1. Make sure the virtual environment is activated:
```bash
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate.bat  # Windows
```

2. Edit the configuration file (`config/config.json`) with your YouTube URLs

3. Run the bot:
```bash
python run.py
```

4. Monitor the logs in the `logs/` directory or in the console output

## Features Explained

### Auto Dependency Checking
The bot automatically checks if all required packages are installed before running.

### ChromeDriver Auto-Updates
The bot uses `undetected-chromedriver` which automatically downloads and updates ChromeDriver to match your Chrome browser version.

### Proxy Rotation
Add proxies to the `proxies` array in the config file. The bot will randomly select proxies when `rotate_proxy` is enabled.

### User-Agent Rotation
When enabled, the bot uses random user-agents to make requests appear more natural.

### Error Handling
The bot includes comprehensive error handling with retry logic. Failed videos will be retried up to `max_retries` times.

### Logging
Detailed logs are saved to the `logs/` directory with timestamps. Each run creates a new log file.

## Troubleshooting

### Chrome/ChromeDriver Issues
- Make sure Google Chrome is installed
- The bot will automatically download the correct ChromeDriver version
- If issues persist, try deleting any existing ChromeDriver files

### Dependency Issues
Run the dependency checker manually:
```bash
python -c "from src.modules.dependency_checker import DependencyChecker; dc = DependencyChecker(); dc.check_all_dependencies()"
```

### Proxy Issues
- Verify proxy format: `host:port` or `user:pass@host:port`
- Test proxies individually before adding them
- Set `rotate_proxy` to `false` to disable proxy usage

### Video Not Playing
- Check if the YouTube URL is valid
- Try disabling headless mode (`"headless": false`)
- Increase `max_retries` in the config

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Be sure to comply with YouTube's Terms of Service and use responsibly. The authors are not responsible for any misuse of this software.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.