#!/usr/bin/env python3
"""Run script for YouTube Viewer Bot."""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(Path(__file__).parent, 'src'))

from youtube_bot import main

if __name__ == "__main__":
    main()
