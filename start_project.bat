@echo off
set "PROJECT_DIR=%~dp0"
echo Starting Backend...
start cmd /k "cd /d "%PROJECT_DIR%backend" && python -m venv venv && call venv\Scripts\activate && pip install -r requirements.txt && uvicorn main:app --reload"

echo Waiting for backend to initialize...
timeout /t 5

echo Starting Frontend...
start "" "%PROJECT_DIR%frontend\index.html"

echo Application Started!
pause
