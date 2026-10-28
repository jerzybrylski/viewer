# The Genesis Order - stage 2 targeted sample collector
# Version 1.0.0 - reads and copies only the explicit allowlist below.
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

function Write-Note {
    param([string]$Message)
    Write-Host $Message
}

try {
    Write-Host ''
    Write-Host 'THE GENESIS ORDER - TARGETED SAMPLE (READ-ONLY)' -ForegroundColor Cyan
    Write-Host 'This script only reads and copies a small allowlist. It does not modify the game.'
    Write-Host 'Do not use it to collect a full installation or media files.'
    Write-Host ''

    $rootInput = (Read-Host 'Paste the authorized game installation folder').Trim().Trim([char[]]@(34, 39))
    if ([string]::IsNullOrWhiteSpace($rootInput)) { throw 'No game folder was provided.' }
    if (-not (Test-Path -LiteralPath $rootInput -PathType Container)) { throw 'The supplied game folder does not exist.' }
    $root = [IO.Path]::GetFullPath($rootInput)

    $systemRelative = 'www\data\System.json'
    $mapInfosRelative = 'www\data\MapInfos.json'
    $systemPath = Join-Path $root $systemRelative
    $mapInfosPath = Join-Path $root $mapInfosRelative
    if (-not (Test-Path -LiteralPath $systemPath -PathType Leaf)) { throw 'Required file not found: www\data\System.json' }
    if (-not (Test-Path -LiteralPath $mapInfosPath -PathType Leaf)) { throw 'Required file not found: www\data\MapInfos.json' }

    # Parse only System.json to locate the configured starting map. No script code is executed.
    $systemText = [IO.File]::ReadAllText($systemPath, [Text.Encoding]::UTF8)
    $system = $systemText | ConvertFrom-Json
    $startMapId = 0
    if ($null -ne $system.startMapId) { $startMapId = [int]$system.startMapId }

    $selected = New-Object 'System.Collections.Generic.List[string]'
    foreach ($relative in @(
        'package.json',
        'www\package.json',
        'www\js\rpg_core.js',
        'www\js\plugins.js',
        'www\data\System.json',
        'www\data\MapInfos.json'
    )) {
        $selected.Add($relative)
    }
    if ($startMapId -gt 0) {
        $mapName = 'Map{0:D3}.json' -f $startMapId
        $selected.Add((Join-Path 'www\data' $mapName))
    }

    $desktop = [Environment]::GetFolderPath('Desktop')
    if ([string]::IsNullOrWhiteSpace($desktop) -or -not (Test-Path -LiteralPath $desktop)) { $desktop = $env:TEMP }
    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
    $outDir = Join-Path $desktop ("TGO_STAGE2_{0}" -f $stamp)
    $zipPath = Join-Path $desktop ("TGO_STAGE2_SAMPLE_{0}.zip" -f $stamp)
    $filesDir = Join-Path $outDir 'files'
    New-Item -ItemType Directory -Path $filesDir -Force | Out-Null

    $manifest = New-Object 'System.Collections.Generic.List[object]'
    $missing = New-Object 'System.Collections.Generic.List[string]'
    foreach ($relative in ($selected | Select-Object -Unique)) {
        $sourcePath = Join-Path $root $relative
        if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
            $missing.Add($relative)
            continue
        }
        $destinationPath = Join-Path $filesDir $relative
        $destinationParent = Split-Path -Parent $destinationPath
        New-Item -ItemType Directory -Path $destinationParent -Force | Out-Null
        Copy-Item -LiteralPath $sourcePath -Destination $destinationPath -Force
        $hash = Get-FileHash -LiteralPath $destinationPath -Algorithm SHA256
        $manifest.Add([pscustomobject]@{
            RelativePath = $relative
            Bytes = [long](Get-Item -LiteralPath $destinationPath).Length
            SHA256 = $hash.Hash.ToLowerInvariant()
        })
    }

    $manifest | Export-Csv -LiteralPath (Join-Path $outDir 'TGO_SAMPLE_MANIFEST.csv') -NoTypeInformation -Encoding UTF8
    $notes = New-Object 'System.Collections.Generic.List[string]'
    $notes.Add('THE GENESIS ORDER - TARGETED SAMPLE')
    $notes.Add('Report version: 1.0.0')
    $notes.Add(('Files copied: {0}' -f $manifest.Count))
    $notes.Add(('Configured starting map ID: {0}' -f $startMapId))
    $notes.Add('Only package/runtime metadata, RPG Maker core version file, plugin configuration, system/map index, and the configured starting map are included.')
    $notes.Add('No full game files, videos, images, audio, saves, or user/account details are included.')
    if ($missing.Count -gt 0) {
        $notes.Add('Some optional allowlist entries were not present:')
        foreach ($item in $missing) { $notes.Add((' - {0}' -f $item)) }
    }
    $notes | Set-Content -LiteralPath (Join-Path $outDir 'TGO_SAMPLE_NOTES.txt') -Encoding UTF8

    Compress-Archive -Path (Join-Path $outDir '*') -DestinationPath $zipPath -CompressionLevel Optimal -Force
    Write-Host ''
    Write-Host 'Finished. Upload only this ZIP to Google Drive:' -ForegroundColor Green
    Write-Host $zipPath -ForegroundColor Green
    Write-Host ("Selected files copied: {0}" -f $manifest.Count)
    Write-Host 'The original game folder was not modified.'
    exit 0
} catch {
    Write-Host ''
    Write-Host ("FAILED: {0}" -f $_.Exception.Message) -ForegroundColor Red
    Write-Host 'No game files were modified.'
    exit 1
}
