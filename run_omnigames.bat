@echo off
REM omniGames Launcher Script for Windows
REM This script starts the omniGames application

setlocal enabledelayedexpansion

REM Get the directory of this script
set SCRIPT_DIR=%~dp0

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python 3.12 or higher is required but not found!
    echo.
    echo Please install Python from https://www.python.org/
    echo Make sure to add Python to your PATH during installation.
    echo.
    pause
    exit /b 1
)

REM Check if pygame is installed
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing required dependencies...
    echo.
    python -m pip install -r "%SCRIPT_DIR%requirements.txt"
    if errorlevel 1 (
        echo Failed to install dependencies!
        pause
        exit /b 1
    )
)

REM Change to script directory
cd /d "%SCRIPT_DIR%"

REM Run the application
python main.py

REM If there's an error, show it
if errorlevel 1 (
    echo.
    echo An error occurred while running omniGames.
    echo Please check that all dependencies are installed.
    echo.
    pause
)

endlocal
