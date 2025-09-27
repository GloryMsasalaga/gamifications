@echo off
REM EduGame SMS - Quick Setup Script for Windows
REM Run this to start Django + ngrok for live demo

echo ========================================
echo  🚀 EduGame SMS - Live Demo Setup
echo ========================================
echo.

REM Check if Django project exists
if not exist "edugame\manage.py" (
    echo ❌ Error: Django project not found!
    echo    Make sure you're in the hackathon directory
    pause
    exit /b 1
)

echo 📋 Starting Django development server...
cd edugame

REM Start Django server in background
start /b "Django Server" cmd /c "python manage.py runserver 0.0.0.0:8000"

echo ⏳ Waiting 5 seconds for Django to start...
timeout /t 5 /nobreak > nul

echo 🔗 Starting ngrok tunnel...
cd ..

REM Start ngrok (this will block and show the tunnel info)
echo.
echo ========================================
echo  📱 Copy the HTTPS URL shown below
echo  🔧 Use it in Africa's Talking webhook
echo ========================================
echo.

ngrok http 8000