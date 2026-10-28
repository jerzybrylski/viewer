# The Genesis Order - read-only installation inventory
# Version 1.0.0
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

$desktop = [Environment]::GetFolderPath('Desktop')
if ([string]::IsNullOrWhiteSpace($desktop) -or -not (Test-Path -LiteralPath $desktop)) {
    $desktop = $env:TEMP
}
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$outDir = Join-Path $desktop ("TGO_INVENTORY_{0}" -f $stamp)
$zipPath = Join-Path $desktop ("TGO_DIAGNOSTIC_{0}.zip" -f $stamp)
$logPath = Join-Path $desktop ("TGO_DIAGNOSTIC_{0}.log" -f $stamp)
$transcriptStarted = $false

function Test-TgoCandidate {
    param([string]$Path)
    if ([string]::IsNullOrWhiteSpace($Path)) { return $false }
    return (Test-Path -LiteralPath $Path -PathType Container)
}

try {
    Start-Transcript -Path $logPath -Force | Out-Null
    $transcriptStarted = $true

    Write-Host ''
    Write-Host 'THE GENESIS ORDER - READ-ONLY INVENTORY' -ForegroundColor Cyan
    Write-Host 'This tool only reads file names and metadata. It does not modify the game.'

    $candidatePaths = New-Object 'System.Collections.Generic.List[string]'
    $programFilesX86 = [Environment]::GetFolderPath([Environment+SpecialFolder]::ProgramFilesX86)
    $programFiles = [Environment]::GetFolderPath([Environment+SpecialFolder]::ProgramFiles)
    $steamRoots = @('C:\Steam', 'D:\Steam', 'C:\SteamLibrary', 'D:\SteamLibrary', 'E:\SteamLibrary', 'F:\SteamLibrary')
    if ($programFilesX86) { $steamRoots += Join-Path $programFilesX86 'Steam' }
    if ($programFiles) { $steamRoots += Join-Path $programFiles 'Steam' }
    $steamRoots = $steamRoots | Select-Object -Unique

    $steamLibraries = New-Object 'System.Collections.Generic.List[string]'
    foreach ($steamRoot in $steamRoots) {
        if (-not (Test-Path -LiteralPath $steamRoot -PathType Container)) { continue }
        $steamLibraries.Add($steamRoot)
        $vdfPath = Join-Path $steamRoot 'steamapps\libraryfolders.vdf'
        if (Test-Path -LiteralPath $vdfPath -PathType Leaf) {
            try {
                $vdf = Get-Content -LiteralPath $vdfPath -Raw -ErrorAction Stop
                foreach ($match in [regex]::Matches($vdf, '"path"\s+"((?:\\.|[^"])*)"')) {
                    $library = $match.Groups[1].Value -replace '\\\\', '\'
                    if (-not [string]::IsNullOrWhiteSpace($library)) { $steamLibraries.Add($library) }
                }
            } catch {
                Write-Host ("Note: could not read Steam library list: {0}" -f $_.Exception.Message) -ForegroundColor Yellow
            }
        }
    }
    foreach ($library in ($steamLibraries | Select-Object -Unique)) {
        $appsDir = Join-Path $library 'steamapps'
        $candidatePaths.Add((Join-Path $appsDir 'common\The Genesis Order'))
        if (Test-Path -LiteralPath $appsDir -PathType Container) {
            foreach ($manifest in (Get-ChildItem -LiteralPath $appsDir -Filter 'appmanifest_*.acf' -File -ErrorAction SilentlyContinue)) {
                try {
                    $manifestText = Get-Content -LiteralPath $manifest.FullName -Raw -ErrorAction Stop
                    if ($manifestText -match '(?im)^\s*"name"\s+"The Genesis Order"\s*$') {
                        $installMatch = [regex]::Match($manifestText, '(?im)^\s*"installdir"\s+"([^"]+)"')
                        if ($installMatch.Success) {
                            $candidatePaths.Add((Join-Path (Join-Path $appsDir 'common') $installMatch.Groups[1].Value))
                        }
                    }
                } catch { }
            }
        }
    }

    $gogBases = @('C:\GOG Games', 'D:\GOG Games', 'E:\GOG Games', 'F:\GOG Games')
    if ($programFilesX86) { $gogBases += Join-Path $programFilesX86 'GOG Galaxy\Games' }
    if ($programFiles) { $gogBases += Join-Path $programFiles 'GOG Galaxy\Games' }
    foreach ($base in $gogBases) {
        $candidatePaths.Add((Join-Path $base 'The Genesis Order'))
    }
    $candidatePaths.Add('C:\Games\The Genesis Order')
    $candidatePaths.Add('D:\Games\The Genesis Order')
    $candidatePaths.Add('E:\Games\The Genesis Order')

    $root = $null
    foreach ($candidate in ($candidatePaths | Select-Object -Unique)) {
        if (Test-TgoCandidate $candidate) {
            $root = (Get-Item -LiteralPath $candidate).FullName
            break
        }
    }

    if (-not $root) {
        Write-Host ''
        Write-Host 'Automatic detection did not find the installation.' -ForegroundColor Yellow
        Write-Host 'Paste the game installation folder, or paste the path to its .exe file.'
        $inputPath = (Read-Host 'Game folder or .exe path').Trim().Trim([char[]]@(34, 39))
        if ([string]::IsNullOrWhiteSpace($inputPath)) { throw 'No game folder was provided.' }
        if (Test-Path -LiteralPath $inputPath -PathType Leaf) {
            $root = Split-Path -LiteralPath $inputPath -Parent
        } elseif (Test-Path -LiteralPath $inputPath -PathType Container) {
            $root = (Get-Item -LiteralPath $inputPath).FullName
        } else {
            throw ("The supplied path does not exist: {0}" -f $inputPath)
        }
    }

    $root = [IO.Path]::GetFullPath($root)
    Write-Host ("Game folder: {0}" -f $root) -ForegroundColor Cyan
    Write-Host ("Report ZIP:  {0}" -f $zipPath) -ForegroundColor Cyan
    Write-Host 'Scanning file names and sizes. No game files will be copied into the report.'

    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
    $scanErrors = @()
    $files = @(Get-ChildItem -LiteralPath $root -File -Recurse -Force -ErrorAction SilentlyContinue -ErrorVariable +scanErrors)
    $rootPrefix = [IO.Path]::GetFullPath($root).TrimEnd([char[]]@('\', '/')) + [IO.Path]::DirectorySeparatorChar
    $inventory = @(
        foreach ($file in $files) {
            $relative = $file.FullName.Substring($rootPrefix.Length)
            if ($file.Extension) { $inventoryExtension = $file.Extension.ToLowerInvariant() } else { $inventoryExtension = '[no extension]' }
            [pscustomobject]@{
                RelativePath = $relative
                Bytes = [long]$file.Length
                Extension = $inventoryExtension
                LastWriteTimeUtc = $file.LastWriteTimeUtc.ToString('o')
            }
        }
    )

    $inventoryPath = Join-Path $outDir 'TGO_FILES.csv'
    $inventory | Export-Csv -LiteralPath $inventoryPath -NoTypeInformation -Encoding UTF8

    $candidateInventory = @($inventory | Where-Object {
        $_.Extension -in @('.json', '.js', '.html', '.htm', '.css', '.txt', '.csv', '.xml', '.ini', '.rpgmvp', '.rpgmvo', '.rpgmvm', '.pak', '.dat') -or
        $_.RelativePath -match '(?i)(^|[\\/])(data|www|wwwroot|content|localization|locale|language|languages|text|script|scripts)([\\/]|$)'
    })
    $candidatePath = Join-Path $outDir 'TGO_POSSIBLE_TEXT_RESOURCES.csv'
    $candidateInventory | Export-Csv -LiteralPath $candidatePath -NoTypeInformation -Encoding UTF8

    $totalBytes = [long](($inventory | Measure-Object -Property Bytes -Sum).Sum)
    $summary = New-Object 'System.Collections.Generic.List[string]'
    $summary.Add('THE GENESIS ORDER - INSTALLATION INVENTORY')
    $summary.Add('Report version: 1.0.0')
    $summary.Add(('Created local time: {0}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')))
    $summary.Add(('Selected game folder: {0}' -f $root))
    $summary.Add(('Files found: {0}' -f $inventory.Count))
    $summary.Add(('Total file size (bytes): {0}' -f $totalBytes))
    $summary.Add(('Total file size (GiB): {0:N3}' -f ($totalBytes / 1GB)))
    $summary.Add(('Possible text/resource entries: {0}' -f $candidateInventory.Count))
    $summary.Add(('Directories with scan warnings: {0}' -f $scanErrors.Count))
    $summary.Add('')
    $summary.Add('FILES BY EXTENSION (top 60, sorted by file count)')
    foreach ($group in ($inventory | Group-Object -Property Extension | Sort-Object Count -Descending | Select-Object -First 60)) {
        $bytes = [long](($group.Group | Measure-Object -Property Bytes -Sum).Sum)
        $summary.Add(("{0}`t{1}`t{2}" -f $group.Name, $group.Count, $bytes))
    }
    $summary.Add('')
    $summary.Add('SIZE BY TOP-LEVEL PATH (top 80, sorted by bytes)')
    $topGroups = $inventory | Group-Object -Property { ($_.RelativePath -split '[\\/]', 2)[0] } | ForEach-Object {
        [pscustomobject]@{ Name = $_.Name; Count = $_.Count; Bytes = [long](($_.Group | Measure-Object -Property Bytes -Sum).Sum) }
    } | Sort-Object Bytes -Descending | Select-Object -First 80
    foreach ($group in $topGroups) {
        $summary.Add(("{0}`t{1}`t{2}" -f $group.Name, $group.Count, $group.Bytes))
    }

    $exeFiles = @(Get-ChildItem -LiteralPath $root -File -Filter '*.exe' -ErrorAction SilentlyContinue)
    $summary.Add('')
    $summary.Add('TOP-LEVEL EXECUTABLE FILES')
    if ($exeFiles.Count -eq 0) { $summary.Add('(none found at the selected folder root)') }
    foreach ($exe in $exeFiles) {
        $version = [Diagnostics.FileVersionInfo]::GetVersionInfo($exe.FullName)
        $summary.Add(("{0}`t{1} bytes`tFileVersion={2}`tProductVersion={3}" -f $exe.Name, $exe.Length, $version.FileVersion, $version.ProductVersion))
    }

    $metadata = [ordered]@{
        reportVersion = '1.0.0'
        createdLocal = (Get-Date -Format 'o')
        gameFolder = $root
        fileCount = $inventory.Count
        totalBytes = $totalBytes
        possibleTextResourceCount = $candidateInventory.Count
        scanWarningCount = $scanErrors.Count
        executables = @($exeFiles | ForEach-Object {
            $v = [Diagnostics.FileVersionInfo]::GetVersionInfo($_.FullName)
            [ordered]@{ name = $_.Name; bytes = [long]$_.Length; fileVersion = $v.FileVersion; productVersion = $v.ProductVersion }
        })
    }
    $metadata | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $outDir 'TGO_METADATA.json') -Encoding UTF8

    $summary | Set-Content -LiteralPath (Join-Path $outDir 'TGO_SUMMARY.txt') -Encoding UTF8
    if ($scanErrors.Count -gt 0) {
        $warningLines = @('Some entries could not be read; the inventory may be incomplete.') + @($scanErrors | ForEach-Object { $_.ToString() })
        $warningLines | Set-Content -LiteralPath (Join-Path $outDir 'TGO_SCAN_WARNINGS.txt') -Encoding UTF8
    }

    Stop-Transcript | Out-Null
    $transcriptStarted = $false
    Copy-Item -LiteralPath $logPath -Destination (Join-Path $outDir 'TGO_RUN_LOG.txt') -Force
    Compress-Archive -Path (Join-Path $outDir '*') -DestinationPath $zipPath -CompressionLevel Optimal -Force

    Write-Host ''
    Write-Host 'Finished successfully.' -ForegroundColor Green
    Write-Host ("Upload this report ZIP to Google Drive: {0}" -f $zipPath) -ForegroundColor Green
    Write-Host 'The ZIP contains file names and metadata only; it does not contain game files.'
    Write-Host 'The game installation was not modified.'
    exit 0
} catch {
    Write-Host ''
    Write-Host ("FAILED: {0}" -f $_.Exception.Message) -ForegroundColor Red
    Write-Host ("Check the log if it was created: {0}" -f $logPath) -ForegroundColor Yellow
    if ($transcriptStarted) {
        try { Stop-Transcript | Out-Null } catch { }
    }
    exit 1
}
