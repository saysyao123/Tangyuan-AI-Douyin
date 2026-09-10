$ErrorActionPreference = 'Stop'

$project = Join-Path $PSScriptRoot 'src\TangyuanDolaStudio\TangyuanDolaStudio.csproj'
$outDir = Join-Path $PSScriptRoot 'publish\win-x64'

if (Test-Path $outDir) {
    Remove-Item $outDir -Recurse -Force
}

Write-Host 'Publishing Tangyuan Dola Studio (win-x64, self-contained, single-file)...'
dotnet publish $project `
    -c Release `
    -r win-x64 `
    --self-contained true `
    -p:PublishSingleFile=true `
    -p:IncludeNativeLibrariesForSelfExtract=true `
    -p:PublishReadyToRun=false `
    -o $outDir

$exe = Join-Path $outDir 'TangyuanDolaStudio.exe'
if (!(Test-Path $exe)) {
    throw "Publish completed but EXE was not found: $exe"
}

Write-Host "OK: $exe"
