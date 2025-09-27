Write-Host "🎮 Starting EduGame SMS Server on Port 3000..." -ForegroundColor Green
Write-Host ""

Set-Location "c:\Users\hp\hackathon\edugame"

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "..\myvenv\Scripts\Activate.ps1"

Write-Host "Starting Django server on port 3000..." -ForegroundColor Yellow
Write-Host "Server will be available at: http://localhost:3000/" -ForegroundColor Cyan
Write-Host "Leaderboard will be at: http://localhost:3000/leaderboard/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host ""

python manage.py runserver 3000