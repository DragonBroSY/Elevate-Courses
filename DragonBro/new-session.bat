@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0new-session.ps1" %*
pause
