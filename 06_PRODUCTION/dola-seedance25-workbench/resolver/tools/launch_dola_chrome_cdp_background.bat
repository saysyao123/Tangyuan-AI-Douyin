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
  exit /b 1
)
if not exist "%PROFILE%" (
  echo [ERROR] Dedicated profile not found: %PROFILE%
  echo [NEXT] Run launch_dola_chrome_cdp.bat once and complete Dola login first.
  exit /b 2
)

echo [INFO] Starting headless Dola Chrome with the existing dedicated profile.
echo [INFO] CDP: http://127.0.0.1:9222
echo [INFO] Close the visible Dola CDP browser before running this launcher.

start "" /b "%CHROME%" ^
  --headless=new ^
  --remote-debugging-port=9222 ^
  --remote-debugging-address=127.0.0.1 ^
  --user-data-dir="%PROFILE%" ^
  --no-first-run ^
  --no-default-browser-check ^
  "%TARGET%"

echo [READY] Background browser launched. Keep this process running.
