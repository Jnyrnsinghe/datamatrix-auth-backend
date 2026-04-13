@echo off
cd /d "%~dp0"
if "%~1"=="" (
  echo Usage: seed_user.bat username password "Full Name"
  pause
  exit /b 1
)
python create_user.py %*
pause
