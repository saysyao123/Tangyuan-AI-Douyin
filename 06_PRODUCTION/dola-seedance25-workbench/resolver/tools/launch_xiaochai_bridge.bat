@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0launch_xiaochai_bridge.ps1"
if errorlevel 1 pause
endlocal
