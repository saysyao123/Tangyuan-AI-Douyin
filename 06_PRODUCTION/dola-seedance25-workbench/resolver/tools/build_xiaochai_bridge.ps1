param(
    [string]$SourceBundle = 'LOCAL_DOLA_PROJECT_ROOT\analysis\小柴多开器3.4.8\bundle',
    [string]$SourceRuntime = 'LOCAL_DOLA_PROJECT_ROOT\analysis_runtime\Xiaochai-3.4.8-bundle',
    [string]$ProjectRoot = 'LOCAL_DOLA_PROJECT_ROOT\dola-original-resolver',
    [string]$OutputRoot = 'LOCAL_DOLA_PROJECT_ROOT\dola-original-resolver\runtime\xiaochai-bridge'
)

$ErrorActionPreference = 'Stop'
$sourceAsar = Join-Path $SourceBundle 'resources\app.asar'
$sourceExe = Join-Path $SourceBundle 'Xiaochai Multi Launcher 3.5.exe'
$sourceElevate = Join-Path $SourceBundle 'resources\elevate.exe'
$stageRoot = Join-Path $ProjectRoot 'runtime\xiaochai-bridge-build'
$stageApp = Join-Path $stageRoot 'app'
$bridgeSource = Join-Path $ProjectRoot 'legacy-host\xiaochai-bridge\xiaochai-bridge.js'
$injector = Join-Path $ProjectRoot 'tools\inject_xiaochai_bridge.mjs'
$npx = (Get-Command npx -ErrorAction Stop).Source

foreach ($required in @($sourceAsar, $sourceExe, $sourceElevate, $bridgeSource, $injector)) {
    if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
        throw "required build input not found: $required"
    }
}
if (-not (Test-Path -LiteralPath $SourceRuntime -PathType Container)) {
    throw "required runtime directory not found: $SourceRuntime"
}

New-Item -ItemType Directory -Path $stageRoot -Force | Out-Null
New-Item -ItemType Directory -Path $OutputRoot -Force | Out-Null
$stageApp = Join-Path $stageRoot ('app-' + [DateTime]::Now.ToString('yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $stageApp -Force | Out-Null

& $npx --yes @electron/asar extract $sourceAsar $stageApp
if ($LASTEXITCODE -ne 0) { throw "asar extraction failed with exit code $LASTEXITCODE" }

Copy-Item -LiteralPath $bridgeSource -Destination (Join-Path $stageApp 'src\xiaochai-bridge.js') -Force
& node $injector (Join-Path $stageApp 'src\main.js')
if ($LASTEXITCODE -ne 0) { throw "main.js bridge injection failed with exit code $LASTEXITCODE" }
& node --check (Join-Path $stageApp 'src\main.js')
if ($LASTEXITCODE -ne 0) { throw 'injected main.js syntax check failed' }

$outputResources = Join-Path $OutputRoot 'resources'
New-Item -ItemType Directory -Path $outputResources -Force | Out-Null
$outputAsar = Join-Path $outputResources 'app.asar'
if (Test-Path -LiteralPath $outputAsar) { Remove-Item -LiteralPath $outputAsar -Force }
& $npx --yes @electron/asar pack $stageApp $outputAsar
if ($LASTEXITCODE -ne 0) { throw "asar packaging failed with exit code $LASTEXITCODE" }

$outputExe = Join-Path $OutputRoot 'Xiaochai Multi Launcher Bridge.exe'
Get-ChildItem -LiteralPath $SourceRuntime -Force | ForEach-Object {
    if ($_.Name -eq 'resources') { return }
    Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $OutputRoot $_.Name) -Recurse -Force
}
Copy-Item -LiteralPath $sourceExe -Destination $outputExe -Force
Copy-Item -LiteralPath $sourceElevate -Destination (Join-Path $outputResources 'elevate.exe') -Force

Write-Output "XIAOCHAI_BRIDGE_BUILD: PASS"
Write-Output "OUTPUT_EXE: $outputExe"
Write-Output "OUTPUT_ASAR: $outputAsar"
Write-Output "STAGE_APP: $stageApp"
