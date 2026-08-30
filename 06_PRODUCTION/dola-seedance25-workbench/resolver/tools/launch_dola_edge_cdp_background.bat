@echo off
setlocal
set "ROOT=%~dp0.."
set "PROFILE=%ROOT%\runtime\dola-edge-cdp-profile"
set "TARGET=https://www.dola.com/chat/00000000000000000"
set "EDGE="

if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" set "EDGE=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
if not defined EDGE if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" set "EDGE=%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
if not defined EDGE if exist "%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe" set "EDGE=%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"

if not defined EDGE (
  echo [ERROR] Microsoft Edge not found.
  exit /b 1
)
if not exist "%PROFILE%" (
  echo [ERROR] Dedicated profile not found: %PROFILE%
  echo [NEXT] Run launch_dola_edge_cdp.bat once and complete Dola login first.
  exit /b 2
)

echo [INFO] Starting headless Dola Edge with the existing dedicated profile.
echo [INFO] CDP: http://127.0.0.1:9222
echo [INFO] Close the visible Dola CDP browser before running this launcher.

start "" /b "%EDGE%" ^
  --headless=new ^
  --remote-debugging-port=9222 ^
  --remote-debugging-address=127.0.0.1 ^
  --user-data-dir="%PROFILE%" ^
  --no-first-run ^
  --no-default-browser-check ^
  "%TARGET%"

echo [READY] Background browser launched. Keep this process running.
