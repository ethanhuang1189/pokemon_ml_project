@echo off
echo ============================================
echo Pokemon Battle Arena - Full Setup
echo ============================================
echo.
echo Starting Pokemon Showdown server...
echo.

cd ..\showdown-relay\pokemon-showdown

REM Start Showdown in a new window
start "Pokemon Showdown Server" cmd /k "node pokemon-showdown start --no-security"

echo Waiting for Showdown server to start...
timeout /t 5 /nobreak > nul

cd ..\..\web

echo.
echo Starting Flask web server...
echo.
echo The application will be available at:
echo   - Web Interface: http://localhost:5000
echo   - Watch Battles: http://localhost:8000
echo.
echo Press Ctrl+C to stop the Flask server
echo (Showdown server will remain running in separate window)
echo.

python app.py
