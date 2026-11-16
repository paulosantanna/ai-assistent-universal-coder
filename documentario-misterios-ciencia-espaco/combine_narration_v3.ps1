$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

$allNarration = @()
$totalWords = 0
$sceneIndex = 0

for ($i = 1; $i -le 9; $i++) {
    $filename = '{0:D2}_scenes_chapter{1}.json' -f ($i+2), $i
    $jsonText = Get-Content $filename -Raw -Encoding UTF8
    
    # Extract all narration fields with their context
    # Find all "narration" : "..." patterns
    $narrationMatches = [System.Text.RegularExpressions.Regex]::Matches($jsonText, '"narration"\s*:\s*"((?:[^"\\]|\\.)*)"')
    
    # Find all scene metadata
    $sceneMatches = [System.Text.RegularExpressions.Regex]::Matches($jsonText, '"scene"\s*:\s*(\d+)\s*,\s*"chapter"\s*:\s*(\d+)\s*,\s*"title"\s*:\s*"([^"]*)"\s*,\s*"duration_seconds"\s*:\s*(\d+)')
    
    for ($j = 0; $j -lt $sceneMatches.Count; $j++) {
        if ($j -lt $narrationMatches.Count) {
            $narration = $narrationMatches[$j].Groups[1].Value
            $narration = [System.Text.RegularExpressions.Regex]::Unescape($narration)
            
            $sceneMatch = $sceneMatches[$j]
            $words = ($narration -split '\s+').Count
            $totalWords += $words
            $allNarration += [pscustomobject]@{
                chapter = [int]$sceneMatch.Groups[2].Value
                scene = [int]$sceneMatch.Groups[1].Value
                title = $sceneMatch.Groups[3].Value
                duration = [int]$sceneMatch.Groups[4].Value
                narration = $narration
                word_count = $words
            }
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