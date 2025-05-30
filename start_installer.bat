@echo off
title Extra Life Bot Installer
echo.
echo Starting Extra Life Discord Bot installer...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo.
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Run the installer
python simple_installer.py

echo.
echo Installer finished.
pause