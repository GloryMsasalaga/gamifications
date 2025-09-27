# EduGame SMS - Live Demo Setup Script (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🚀 EduGame SMS - Live Demo Setup" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Django project exists
if (-not (Test-Path "edugame\manage.py")) {
    Write-Host "❌ Error: Django project not found!" -ForegroundColor Red
    Write-Host "   Make sure you're in the hackathon directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "📋 Starting Django development server..." -ForegroundColor Green

# Start Django server in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd edugame; python manage.py runserver 0.0.0.0:8000"

Write-Host "⏳ Waiting 5 seconds for Django to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "🔗 Starting ngrok tunnel..." -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  📱 Copy the HTTPS URL shown below" -ForegroundColor Yellow
Write-Host "  🔧 Use it in Africa's Talking webhook" -ForegroundColor Yellow  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start ngrok tunnel
try {
    & ngrok http 8000
} catch {
    Write-Host "❌ Error: ngrok not found!" -ForegroundColor Red
    Write-Host "   Install ngrok first: choco install ngrok" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}