Set-Location $PSScriptRoot

# Auto-increment from highest existing DayN.md
$existing = Get-ChildItem "Day*.md" | Where-Object { $_.Name -match '^Day\d+\.md$' }
$n = if ($existing) {
    ($existing | ForEach-Object { [int]($_.BaseName -replace 'Day','') } | Measure-Object -Maximum).Maximum + 1
} else { 1 }

$date  = Get-Date -Format "yyyy-MM-dd"
$file  = "Day$n.md"

$content = @"
---
publish: false
title: "Day $n"
date: $date
topics: ""
---

#

"@

[System.IO.File]::WriteAllText((Join-Path $PSScriptRoot $file), $content, [System.Text.Encoding]::UTF8)

# Link it from Elevate.md
obsidian append path=Elevate.md "content=[[Day$n]]"

# Open the new note
obsidian open path=$file

Write-Host "Created $file — linked from Elevate.md"
