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
  pause
  exit /b 1
)

if not exist "%PROFILE%" mkdir "%PROFILE%"

echo [INFO] Starting dedicated Dola Edge profile.
echo [INFO] CDP: http://127.0.0.1:9222
echo [INFO] Profile: %PROFILE%
echo [INFO] This is NOT your normal Edge profile.

start "" "%EDGE%" ^
  --remote-debugging-port=9222 ^
  --remote-debugging-address=127.0.0.1 ^
  --user-data-dir="%PROFILE%" ^
  --no-first-run ^
  --no-default-browser-check ^
  "%TARGET%"

echo.
echo [NEXT] Complete Dola login in the opened Edge window if needed.
echo [NEXT] Keep this browser open, then run the Codex P1.2 CDP capture command.
pause
