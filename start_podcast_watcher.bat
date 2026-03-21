@echo off
title Elevate Podcast Watcher
cd /d "%~dp0"
"%USERPROFILE%\anaconda3\python.exe" podcast_upload.py
pause
