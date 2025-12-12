# Quick Start Guide

## Setup (5 minutes)

### Option 1: Automated Setup (Recommended)

**Linux/macOS:**
```bash
./setup_venv.sh
source venv/bin/activate
```

**Windows:**
```cmd
setup_venv.bat
venv\Scripts\activate.bat
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Configuration (2 minutes)

1. Open `config/config.json` in a text editor
2. Replace the example URL with your YouTube video URL(s):
   ```json
   "youtube_urls": [
     "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
   ]
   ```
3. (Optional) Configure other settings:
   - Adjust watch times in `delays` section
   - Add proxies to `proxies` array
   - Set `headless` to `true` for background mode

## Run (30 seconds)

```bash
# Make sure venv is activated
python run.py
```

That's it! The bot will:
1. ✓ Check dependencies
2. ✓ Load configuration
3. ✓ Setup Chrome browser
4. ✓ Watch your videos
5. ✓ Log everything to `logs/` directory

## Example Configurations

### Watch a single video for 60 seconds
```json
{
  "youtube_urls": ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"],
  "delays": {
    "min_watch_time": 60,
    "max_watch_time": 60
  }
}
```

### Watch multiple videos with random delays
```json
{
  "youtube_urls": [
    "https://www.youtube.com/watch?v=video1",
    "https://www.youtube.com/watch?v=video2",
    "https://www.youtube.com/watch?v=video3"
  ],
  "delays": {
    "min_watch_time": 30,
    "max_watch_time": 120,
    "min_delay_between_videos": 10,
    "max_delay_between_videos": 30
  }
}
```

### Headless mode (no browser window)
```json
{
  "youtube_urls": ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"],
  "browser": {
    "headless": true
  }
}
```

### With proxy and user-agent rotation
```json
{
  "youtube_urls": ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"],
  "proxies": ["proxy.example.com:8080"],
  "rotation": {
    "rotate_user_agent": true,
    "rotate_proxy": true
  }
}
```

## Troubleshooting

**Problem:** `ModuleNotFoundError`
**Solution:** Make sure virtual environment is activated and dependencies are installed

**Problem:** Chrome/ChromeDriver issues
**Solution:** Make sure Google Chrome browser is installed. ChromeDriver will auto-update.

**Problem:** Video not playing
**Solution:** Set `"headless": false` in config to see what's happening

## Monitoring

- Check console output for real-time status
- Check `logs/` directory for detailed logs
- Each run creates a new timestamped log file

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Customize `config/config.json` for your needs
3. Check the `src/modules/` directory to understand the code structure
