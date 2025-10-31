@echo off
echo ========================================
echo AI Skills Academy - Quick Start
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.7+
    pause
    exit /b
)
echo.

echo Checking for .env file...
if not exist .env (
    echo.
    echo ========================================
    echo WARNING: .env file not found!
    echo ========================================
    echo.
    echo Creating .env from example...
    if exist .env.example (
        copy .env.example .env
        echo.
        echo .env file created! Please edit it and add your Gemini API key.
        echo.
        echo 1. Get FREE API key: https://makersuite.google.com/app/apikey
        echo 2. Open .env file and replace "your_gemini_api_key_here" with your actual key
        echo 3. Run this script again
        echo.
        pause
        exit /b
    ) else (
        echo.
        echo Creating new .env file...
        echo GEMINI_API_KEY=your_gemini_api_key_here > .env
        echo SECRET_KEY=your-secret-key-here >> .env
        echo.
        echo .env file created! Please edit it and add your Gemini API key.
        echo.
        echo 1. Get FREE API key: https://makersuite.google.com/app/apikey
        echo 2. Open .env file and replace "your_gemini_api_key_here" with your actual key
        echo 3. Run this script again
        echo.
        pause
        exit /b
    )
)
echo .env file found!
echo.

echo Installing dependencies...
pip install -r requirements.txt -q
echo.

echo Starting server...
echo.
echo ========================================
echo Server will start on:
echo http://localhost:5000
echo ========================================
echo.
echo If you see "✓ Gemini API key loaded successfully"
echo then everything is configured correctly!
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
python app.py
