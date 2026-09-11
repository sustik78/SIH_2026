@echo off
title PRAMAN AI - Starting Platform...
color 0A
echo ====================================================================
echo         STARTING PRAMAN AI (LEGAL METROLOGY INSPECTION)
echo ====================================================================
echo.

:: Navigate to directory where this script is located
cd /d "%~dp0"

echo [1/3] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "PRAMAN AI - Backend (Port 8000)" cmd /k "python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000"

echo [2/3] Starting Vite Frontend on http://localhost:5173 ...
start "PRAMAN AI - Frontend (Port 5173)" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo [3/3] Waiting for servers to initialize...
timeout /t 3 /nobreak >nul

echo.
echo Launching PRAMAN AI in your default web browser...
start http://localhost:5173/

echo.
echo ====================================================================
echo  PRAMAN AI IS READY!
echo  - Frontend UI : http://localhost:5173/
echo  - Backend API : http://127.0.0.1:8000/
echo  - Swagger Docs: http://127.0.0.1:8000/docs
echo ====================================================================
echo.
echo (You may close this launcher window now, or press any key to exit)
pause >nul
