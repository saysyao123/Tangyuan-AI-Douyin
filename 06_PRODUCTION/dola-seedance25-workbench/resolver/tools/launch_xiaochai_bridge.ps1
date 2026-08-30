$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$exe = Join-Path $projectRoot 'runtime\xiaochai-bridge\Xiaochai Multi Launcher Bridge.exe'
if (-not (Test-Path -LiteralPath $exe -PathType Leaf)) {
    throw "Bridge build not found. Run tools\build_xiaochai_bridge.ps1 first."
}
$env:XIAOCHAI_DOLA_BRIDGE_ENABLED = '1'
$env:XIAOCHAI_DOLA_BRIDGE_PORT = '8766'
$env:XIAOCHAI_DOLA_BRIDGE_OUTPUT_DIR = Join-Path $projectRoot 'captures\legacy-host'
New-Item -ItemType Directory -Path $env:XIAOCHAI_DOLA_BRIDGE_OUTPUT_DIR -Force | Out-Null
Start-Process -FilePath $exe -WorkingDirectory (Split-Path -Parent $exe)
Write-Output "XIAOCHAI_BRIDGE_LAUNCH: PASS"
Write-Output "BRIDGE_ENDPOINT: http://127.0.0.1:8766"
Write-Output "MANUAL_LOGIN: use the cloned Xiaochai window and complete Dola login yourself"
