param(
    [string]$Start = "2026-08-10",
    [string]$End = "2026-08-25",
    [switch]$ForceLogin
)

$ErrorActionPreference = "Stop"
$R3Dir = $PSScriptRoot
$RepoRoot = (Resolve-Path (Join-Path $R3Dir "..\..\..")).Path
$VenvDir = Join-Path $RepoRoot ".venv-r3-douyin"
$Python = Join-Path $VenvDir "Scripts\python.exe"
$SecretFile = Join-Path $R3Dir ".secrets\douyin_cookie.txt"
$LocalRaw = Join-Path $R3Dir ".local_raw"
$SqliteOut = Join-Path $LocalRaw "r3_douyin.sqlite3"
$F2Commit = "7dab3e2ffffaa2535834d28fca99dbc2e89fa9d3"

function Step([string]$Text) {
    Write-Host ""
    Write-Host "=== $Text ===" -ForegroundColor Cyan
}

Step "R3 Douyin authenticated data refresh"
Write-Host "Repo:   $RepoRoot"
Write-Host "Window: $Start -> $End (end exclusive)"

if (-not (Test-Path $Python)) {
    Step "Create local Python environment"
    py -3.11 -m venv $VenvDir
}

Step "Install pinned collectors"
& $Python -m pip install --disable-pip-version-check --quiet --upgrade pip
& $Python -m pip install --disable-pip-version-check --quiet "git+https://github.com/Johnserf-Seed/f2.git@$F2Commit" playwright
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }

if ($ForceLogin -or -not (Test-Path $SecretFile)) {
    Step "One-time Douyin QR login"
    & $Python -m playwright install chromium
    if ($LASTEXITCODE -ne 0) { throw "Playwright Chromium installation failed." }
    $loginArgs = @((Join-Path $R3Dir "tools\setup_douyin_cookie.py"))
    if ($ForceLogin) { $loginArgs += "--force" }
    & $Python @loginArgs
    if ($LASTEXITCODE -ne 0) { throw "Douyin login bootstrap failed." }
}

Step "Authenticated 9-account collection"
& $Python (Join-Path $R3Dir "tools\collect_core_accounts_f2_auth.py") --start $Start --end $End
$CollectCode = $LASTEXITCODE
if ($CollectCode -ne 0) {
    Write-Host ""
    Write-Host "Authenticated data Gate is not closed." -ForegroundColor Yellow
    Write-Host "If the report shows PROFILE/FIRST_PAGE auth failure, rerun:" -ForegroundColor Yellow
    Write-Host ".\06_TESTS\MV\WEB_R3\run_douyin_refresh.ps1 -ForceLogin" -ForegroundColor Yellow
    exit $CollectCode
}

Step "Normalize SONG_FAMILY at work level"
& $Python (Join-Path $R3Dir "database\normalize_songs.py")
if ($LASTEXITCODE -ne 0) { throw "Song normalization failed." }

Step "Build and validate SQLite analysis database"
New-Item -ItemType Directory -Force -Path $LocalRaw | Out-Null
& $Python (Join-Path $R3Dir "database\build_sqlite.py") --data-dir (Join-Path $R3Dir "database") --out $SqliteOut
if ($LASTEXITCODE -ne 0) { throw "SQLite build/foreign-key validation failed." }

Step "Run repeat/trend analysis"
& $Python (Join-Path $R3Dir "database\analyze_song_repeats.py")
$AnalysisCode = $LASTEXITCODE
if ($AnalysisCode -ne 0) {
    Write-Host "Analysis completed but HG01 data Gate remains blocked." -ForegroundColor Yellow
    exit $AnalysisCode
}

Step "R3 data refresh PASS"
Write-Host "All 9 core accounts passed authenticated collection and window closure." -ForegroundColor Green
Write-Host "Canonical database files were updated under:"
Write-Host "  $R3Dir\database"
Write-Host "Generated local SQLite:"
Write-Host "  $SqliteOut"
Write-Host "Next: review direct_douyin_evidence.json and open HG01 only after candidate QA."
