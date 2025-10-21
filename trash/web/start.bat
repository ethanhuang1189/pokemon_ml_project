@echo off
echo Starting Pokemon Battle Website...
echo.
echo Starting Showdown server on port 8000...
start /B cmd /c "cd ..\showdown-relay && node server.js"

echo Waiting for Showdown server to start...
timeout /t 3 /nobreak > nul

echo Starting Flask web server on port 5000...
echo.
echo Website will be available at: http://localhost:5000
echo.
python app.py
