param([string]$Title = "")
Set-Location $PSScriptRoot

if ($Title -eq "") {
    $Title = Read-Host "Session title (e.g. 'Steep Turns', 'ATP Ground School')"
}

$date    = Get-Date -Format "yyyy-MM-dd"
$file    = "$date - $Title.md"
$outPath = Join-Path $PSScriptRoot "Sessions\$file"

$content = @"
# $date — $Title
Tags: #session

## Project


## Goal


## What We Did
-

## Decisions Made
-

## Next Steps
- [ ]

## Related
-
"@

[System.IO.File]::WriteAllText($outPath, $content, [System.Text.Encoding]::UTF8)

# Path is relative to vault root (Obsidian Vault)
obsidian open "path=DragonBro/Sessions/$file"
Write-Host "Opened: DragonBro/Sessions/$file"
