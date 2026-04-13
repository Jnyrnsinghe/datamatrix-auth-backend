@echo off
cd /d "%~dp0"
if not exist ".env" (
  echo Missing .env file. Copy .env.example to .env and fill in your secrets first.
  pause
  exit /b 1
)
python -m uvicorn app.main:app --reload
