@echo off
setlocal
cd /d "%~dp0"
npm run start -- --background --enable-experimental-dola
endlocal
