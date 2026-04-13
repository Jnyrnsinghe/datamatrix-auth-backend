@echo off
cd /d "%~dp0"
if exist ".env" (
  echo .env already exists.
  pause
  exit /b 0
)
copy ".env.example" ".env" >nul
echo Created .env from .env.example
echo Edit .env and add your real secrets before starting the backend.
pause
