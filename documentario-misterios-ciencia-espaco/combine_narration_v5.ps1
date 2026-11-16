$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

$allNarration = @()
$totalWords = 0

for ($i = 1; $i -le 9; $i++) {
    $filename = '{0:D2}_scenes_chapter{1}.json' -f ($i+2), $i
    $jsonText = Get-Content $filename -Raw -Encoding UTF8
    
    # Extract scene objects using a more permissive regex that handles UTF-8
    # Match: "scene": N, "chapter": N, "title": "...", "narration": "...", "duration_seconds": N
    $pattern = '"scene"\s*:\s*(\d+)\s*,\s*"chapter"\s*:\s*(\d+)\s*,\s*"title"\s*:\s*"([^"]*)"\s*,\s*"narration"\s*:\s*"((?:[^"\\]|\\.)*)"\s*,\s*"visual"\s*:\s*"((?:[^"\\]|\\.)*)"\s*,\s*"duration_seconds"\s*:\s*(\d+)'
    $matches = [System.Text.RegularExpressions.Regex]::Matches($jsonText, $pattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
    
    foreach ($match in $matches) {
        $narration = $match.Groups[4].Value
        # Handle escaped characters
        $narration = $narration -replace '\\"', '"' -replace '\\\\', '\' -replace '\\n', "`n" -replace '\\t', "`t" -replace '\\r', "`r"
        # Handle Unicode escapes
        $narration = [System.Text.RegularExpressions.Regex]::Replace($narration, '\\u([0-9a-fA-F]{4})', { 
            param($m) [char]::Parse([int]::Parse($m.Groups[1].Value, [System.Globalization.NumberStyles]::HexNumber)).ToString() 
        })
        
        $words = ($narration -split '\s+').Count
        $totalWords += $words
        $allNarration += [pscustomobject]@{
            chapter = [int]$match.Groups[2].Value
            scene = [int]$match.Groups[1].Value
            title = $match.Groups[3].Value
            duration = [int]$match.Groups[6].Value
            narration = $narration
            word_count = $words
        }
    }
}

$output = "MISTÉRIOS DA CIÊNCIA E DO ESPAÇO`nDocumentário de 90 minutos - Roteiro Completo`n" + ('=' * 60) + "`n`n"
foreach ($item in $allNarration) {
    $output += "[CAPÍTULO {0} - CENA {1}] {2}`n" -f $item.chapter, $item.scene, $item.title
    $output += "Duração: {0}s | Palavras: {1}`n" -f $item.duration, $item.word_count
    $output += "{0}`n`n" -f $item.narration
}

Set-Content -Path 'full_narration.txt' -Value $output -Encoding UTF8

Write-Host "Total scenes: $($allNarration.Count)"
Write-Host "Total words: $totalWords"
Write-Host "Average words per minute: $([math]::Round($totalWords / 90, 1))"
Write-Host "Target words per minute: 125"
Write-Host "Expected duration at 125 wpm: $([math]::Round($totalWords / 125, 1)) minutes"