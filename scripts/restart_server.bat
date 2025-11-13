@echo off
REM Restart the Uvicorn server with fresh environment variables

echo Stopping any running servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq uvicorn*" 2>nul

echo.
echo Starting server with fresh environment variables...
echo.

cd /d "%~dp0.."
.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
