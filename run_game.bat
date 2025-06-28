@echo off
REM Quick start script for Windows users
REM Retro Platform Fighter - Diamond Quest

echo.
echo ========================================
echo  Retro Platform Fighter - Diamond Quest
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Checking Python version...
python --version

echo.
echo Installing/updating dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Error: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Starting game...
python retro_platform_game.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start game
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo Thanks for playing!
pause
