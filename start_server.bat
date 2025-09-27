@echo off
echo 🎮 Starting EduGame SMS Server on Port 3000...
echo.

cd /d "c:\Users\hp\hackathon\edugame"

echo Activating virtual environment...
call "..\myvenv\Scripts\activate"

echo Starting Django server on port 3000...
echo Server will be available at: http://localhost:3000/
echo Leaderboard will be at: http://localhost:3000/leaderboard/
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver 3000