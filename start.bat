@echo off
echo Starting CarPredict Server...
cd /d "C:\Users\soume\OneDrive\Desktop\Car price prediction\MyCarPrediction"
start cmd /k "python Backend/app.py"
timeout /t 8
start http://127.0.0.1:8000/index.html
echo Server Started!
pause
