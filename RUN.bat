@echo off
echo ================================
echo AI Skills Academy - Quick Start
echo ================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.7+
    pause
    exit /b
)
echo.

echo Installing Flask (if needed)...
pip install Flask -q
echo.

echo Starting server...
echo.
echo ================================
echo Server will start on:
echo http://localhost:5000
echo ================================
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
python app.py
