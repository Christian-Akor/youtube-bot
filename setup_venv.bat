@echo off
REM Setup script for YouTube Viewer Bot (Windows)

echo ==========================================
echo YouTube Viewer Bot - Setup
echo ==========================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

echo Using Python:
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ==========================================
echo Setup completed successfully!
echo ==========================================
echo.
echo To run the bot:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate.bat
echo   2. Run the bot:
echo      python run.py
echo.
echo To deactivate the virtual environment:
echo   deactivate
echo.

pause
