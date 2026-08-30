@echo off
setlocal
set "ROOT=%~dp0.."
set "PROFILE=%ROOT%\runtime\dola-cdp-profile"
set "TARGET=https://www.dola.com/chat/00000000000000000"
set "CHROME="

if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" set "CHROME=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
if not defined CHROME if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" set "CHROME=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
if not defined CHROME if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" set "CHROME=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"

if not defined CHROME (
  echo [ERROR] Google Chrome not found.
  echo Try launch_dola_edge_cdp.bat instead.
  pause
  exit /b 1
)

if not exist "%PROFILE%" mkdir "%PROFILE%"

echo [INFO] Starting dedicated Dola Chrome profile.
echo [INFO] CDP: http://127.0.0.1:9222
echo [INFO] Profile: %PROFILE%
echo [INFO] This is NOT your normal Chrome profile.

start "" "%CHROME%" ^
  --remote-debugging-port=9222 ^
  --remote-debugging-address=127.0.0.1 ^
  --user-data-dir="%PROFILE%" ^
  --no-first-run ^
  --no-default-browser-check ^
  "%TARGET%"

echo.
echo [NEXT] Complete Dola login in the opened Chrome window if needed.
echo [NEXT] Keep this browser open, then run the Codex P1.2 CDP capture command.
pause
