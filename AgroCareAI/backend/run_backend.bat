@echo off
set "VENV_PATH=%~dp0..\..\..\..\..\venv"
if exist "%VENV_PATH%\Scripts\python.exe" (
    echo Using venv at "%VENV_PATH%"
    "%VENV_PATH%\Scripts\python.exe" app.py
) else (
    echo ERROR: Virtual environment not found at "%VENV_PATH%"
    pause
)
