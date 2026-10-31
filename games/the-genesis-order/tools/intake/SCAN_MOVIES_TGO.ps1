# The Genesis Order - read-only movie/video call scan
# Version 1.0.0
#
# Znajduje folder `www\data` w instalacji gry i uruchamia statyczny skaner
# `scan_movie_calls.py` z repozytorium. Skrypt czyta wyłącznie pliki JSON danych
# gry, niczego nie zmienia, nie uruchamia gry ani jej kodu i nie kopiuje assetów.
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$scanner = Join-Path (Split-Path -Parent $here) 'scan_movie_calls.py'
$desktop = [Environment]::GetFolderPath('Desktop')
if ([string]::IsNullOrWhiteSpace($desktop) -or -not (Test-Path -LiteralPath $desktop)) {
    $desktop = $env:TEMP
}
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$outPath = Join-Path $desktop ("TGO_movie_calls_{0}.json" -f $stamp)

function Find-Python {
    foreach ($candidate in @('py', 'python', 'python3')) {
        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($command) {
            $arguments = if ($candidate -eq 'py') { @('-3', '--version') } else { @('--version') }
            try {
                & $command.Source @arguments *> $null
                if ($LASTEXITCODE -eq 0) { return $command.Source }
            } catch { }
        }
    }
    return $null
}

function Test-GameData {
    param([string]$Path)
    if ([string]::IsNullOrWhiteSpace($Path)) { return $false }
    return (Test-Path -LiteralPath (Join-Path $Path 'www\data\CommonEvents.json') -PathType Leaf)
}

Write-Host ''
Write-Host 'THE GENESIS ORDER - SKAN WSTAWEK WIDEO (TYLKO ODCZYT)' -ForegroundColor Cyan
Write-Host 'Skrypt czyta pliki danych gry i zapisuje maly raport JSON. Niczego nie zmienia.'
Write-Host ''

if (-not (Test-Path -LiteralPath $scanner -PathType Leaf)) {
    Write-Host ("Nie znaleziono skanera: {0}" -f $scanner) -ForegroundColor Red
    Write-Host 'Uruchom ten skrypt z katalogu tools/intake w repozytorium projektu.'
    Read-Host 'Nacisnij Enter, aby zakonczyc'
    exit 1
}

$python = Find-Python
if (-not $python) {
    Write-Host 'Nie znaleziono Pythona 3. Zainstaluj Python 3 albo zamiast tego przeslij plik data.zip.' -ForegroundColor Yellow
    Read-Host 'Nacisnij Enter, aby zakonczyc'
    exit 1
}

$candidates = New-Object 'System.Collections.Generic.List[string]'
$programFilesX86 = [Environment]::GetFolderPath([Environment+SpecialFolder]::ProgramFilesX86)
$programFiles = [Environment]::GetFolderPath([Environment+SpecialFolder]::ProgramFiles)
$roots = @('C:\', 'D:\', 'E:\', 'F:\')
foreach ($root in $roots) {
    if (-not (Test-Path -LiteralPath $root -PathType Container)) { continue }
    foreach ($library in @('SteamLibrary', 'Steam', 'GOG Games', 'Games')) {
        $candidates.Add((Join-Path $root (Join-Path $library 'The Genesis Order')))
    }
    $candidates.Add((Join-Path $root 'The Genesis Order'))
}
if ($programFilesX86) { $candidates.Add((Join-Path $programFilesX86 'Steam\steamapps\common\The Genesis Order')) }
if ($programFiles) { $candidates.Add((Join-Path $programFiles 'Steam\steamapps\common\The Genesis Order')) }

$gamePath = $null
foreach ($candidate in ($candidates | Select-Object -Unique)) {
    if (Test-GameData $candidate) { $gamePath = $candidate; break }
}

while (-not $gamePath) {
    Write-Host ''
    Write-Host 'Nie znalazlem folderu gry automatycznie.'
    $answer = Read-Host 'Podaj folder instalacji gry (ten, w ktorym jest plik.exe i folder www) albo Enter, aby przerwac'
    if ([string]::IsNullOrWhiteSpace($answer)) {
        Write-Host 'Przerwano bez zapisu.'
        Read-Host 'Nacisnij Enter, aby zakonczyc'
        exit 1
    }
    $answer = $answer.Trim('"', ' ')
    if (Test-Path -LiteralPath (Join-Path $answer 'data\CommonEvents.json') -PathType Leaf) {
        $answer = Split-Path -Parent $answer
    }
    if (Test-GameData $answer) { $gamePath = $answer }
    else { Write-Host 'W tym folderze nie ma www\data\CommonEvents.json. Sprobuj ponownie.' -ForegroundColor Yellow }
}

Write-Host ''
Write-Host ("Instalacja: {0}" -f $gamePath) -ForegroundColor Green
Write-Host 'Skanuje pliki danych (bez uruchamiania gry)...'

$dataDir = Join-Path $gamePath 'www\data'
& $python $scanner --data-dir $dataDir --out $outPath
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Skan nie zakonczyl sie poprawnie. Skopiuj komunikat bledu powyzej.' -ForegroundColor Red
    Read-Host 'Nacisnij Enter, aby zakonczyc'
    exit $LASTEXITCODE
}

Write-Host ''
Write-Host ("Raport: {0}" -f $outPath) -ForegroundColor Green
Write-Host 'Przeslij ten pojedynczy plik JSON (kilka kB) do projektu. Nie wysylaj folderu gry.'
Read-Host 'Nacisnij Enter, aby zakonczyc'
exit 0
