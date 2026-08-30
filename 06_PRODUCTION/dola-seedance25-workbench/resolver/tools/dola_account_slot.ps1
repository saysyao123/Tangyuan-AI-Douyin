param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^A[0-9]{2}$')]
    [string]$AccountId,
    [ValidateSet('Login', 'Background', 'Status')]
    [string]$Mode = 'Status',
    [string]$TargetUrl = 'https://www.dola.com/chat/'
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Number = [int]$AccountId.Substring(1, 2)
$SessionSlot = 'S{0:D2}' -f $Number
$Port = 9330 + $Number
$Profile = Join-Path $Root (Join-Path 'runtime\dola-accounts' $AccountId)
$Endpoint = "http://127.0.0.1:$Port"

if ($TargetUrl -notmatch '^https://([a-z0-9-]+\.)?dola\.com(/|$)') {
    throw 'TargetUrl must be an HTTPS dola.com URL.'
}

if ($Mode -eq 'Status') {
    try {
        $version = Invoke-RestMethod -Uri "$Endpoint/json/version" -TimeoutSec 3
        [pscustomobject]@{
            account_id = $AccountId
            session_slot = $SessionSlot
            endpoint = $Endpoint
            profile_dir = $Profile
            profile_exists = Test-Path -LiteralPath $Profile
            cdp_ready = $true
            browser = [string]$version.Browser
        } | ConvertTo-Json -Depth 4
    } catch {
        [pscustomobject]@{
            account_id = $AccountId
            session_slot = $SessionSlot
            endpoint = $Endpoint
            profile_dir = $Profile
            profile_exists = Test-Path -LiteralPath $Profile
            cdp_ready = $false
            browser = $null
        } | ConvertTo-Json -Depth 4
    }
    exit 0
}

$BrowserCandidates = @(
    (Join-Path $env:ProgramFiles 'Google\Chrome\Application\chrome.exe'),
    (Join-Path ${env:ProgramFiles(x86)} 'Google\Chrome\Application\chrome.exe'),
    (Join-Path $env:LOCALAPPDATA 'Google\Chrome\Application\chrome.exe'),
    (Join-Path ${env:ProgramFiles(x86)} 'Microsoft\Edge\Application\msedge.exe'),
    (Join-Path $env:ProgramFiles 'Microsoft\Edge\Application\msedge.exe'),
    (Join-Path $env:LOCALAPPDATA 'Microsoft\Edge\Application\msedge.exe')
)
$Browser = $BrowserCandidates | Where-Object { $_ -and (Test-Path -LiteralPath $_) } | Select-Object -First 1
if (-not $Browser) {
    throw 'Chrome or Edge was not found.'
}

$Existing = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($Existing) {
    throw "Session slot $SessionSlot is already listening on $Endpoint. Close that slot before relaunching it."
}

New-Item -ItemType Directory -Force -Path $Profile | Out-Null
$Arguments = @(
    '--no-first-run',
    '--no-default-browser-check',
    '--remote-debugging-address=127.0.0.1',
    "--remote-debugging-port=$Port",
    "--user-data-dir=$Profile",
    $TargetUrl
)
if ($Mode -eq 'Background') {
    $Arguments = @('--headless=new') + $Arguments
    $windowStyle = 'Hidden'
} else {
    $windowStyle = 'Normal'
}

$process = Start-Process -FilePath $Browser -ArgumentList $Arguments -WindowStyle $windowStyle -PassThru
[pscustomobject]@{
    account_id = $AccountId
    session_slot = $SessionSlot
    endpoint = $Endpoint
    profile_dir = $Profile
    mode = $Mode
    process_id = $process.Id
    manual_login_required = ($Mode -eq 'Login')
    note = if ($Mode -eq 'Login') { 'Complete Dola login manually, then close this browser before using Background mode.' } else { 'Background slot started; attach the resolver to this endpoint.' }
} | ConvertTo-Json -Depth 4
