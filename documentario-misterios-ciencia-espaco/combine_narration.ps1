$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

$allNarration = @()
$totalWords = 0

for ($i = 1; $i -le 9; $i++) {
    $filename = '{0:D2}_scenes_chapter{1}.json' -f ($i+2), $i
    $jsonText = Get-Content $filename -Raw -Encoding UTF8
    
    # Use regex to extract narration fields
    $matches = [System.Text.RegularExpressions.Regex]::Matches($jsonText, '"narration"\s*:\s*"((?:[^"\\]|\\.)*)"')
    foreach ($match in $matches) {
        $narration = $match.Groups[1].Value
        # Unescape JSON escape sequences
        $narration = $narration -replace '\\u00e7', 'ç' -replace '\\u00e3', 'ã' -replace '\\u00f5', 'õ' -replace '\\u00e1', 'á' -replace '\\u00e9', 'é' -replace '\\u00ed', 'í' -replace '\\u00f3', 'ó' -replace '\\u00fa', 'ú' -replace '\\u00ea', 'ê' -replace '\\u00f4', 'ô' -replace '\\u00e0', 'à' -replace '\\u00ee', 'î' -replace '\\u00fb', 'û' -replace '\\u00c7', 'Ç' -replace '\\u00c3', 'Ã' -replace '\\u00d5', 'Õ' -replace '\\u00c1', 'Á' -replace '\\u00c9', 'É' -replace '\\u00cd', 'Í' -replace '\\u00d3', 'Ó' -replace '\\u00da', 'Ú' -replace '\\u00ca', 'Ê' -replace '\\u00d4', 'Ô' -replace '\\u00c0', 'À' -replace '\\"', '"' -replace '\\\\', '\'
        
        # Also extract other fields for this scene using the scene index
        $sceneIndex = $allNarration.Count + 1
        $sceneMatch = [System.Text.RegularExpressions.Regex]::Match($jsonText, '"scene"\s*:\s*(\d+).*?"chapter"\s*:\s*(\d+).*?"title"\s*:\s*"([^"]*)".*?"duration_seconds"\s*:\s*(\d+)', [System.Text.RegularExpressions.RegexOptions]::Singleline)
        
        # Simpler: just count words and add to collection
        $words = ($narration -split '\s+').Count
        $totalWords += $words
        $allNarration += [pscustomobject]@{
            narration = $narration
            word_count = $words
        }
    }
}

# Now get the titles and metadata separately
$sceneInfo = @()
for ($i = 1; $i -le 9; $i++) {
    $filename = '{0:D2}_scenes_chapter{1}.json' -f ($i+2), $i
    $jsonText = Get-Content $filename -Raw -Encoding UTF8
    
    $sceneMatches = [System.Text.RegularExpressions.Regex]::Matches($jsonText, '"scene"\s*:\s*(\d+).*?"chapter"\s*:\s*(\d+).*?"title"\s*:\s*"([^"]*)".*?"duration_seconds"\s*:\s*(\d+)', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    foreach ($match in $sceneMatches) {
        $sceneInfo += [pscustomobject]@{
            scene = [int]$match.Groups[1].Value
            chapter = [int]$match.Groups[2].Value
            title = $match.Groups[3].Value
            duration = [int]$match.Groups[4].Value
        }
    }
}

# Combine narration with scene info
$finalNarration = @()
for ($j = 0; $j -lt $allNarration.Count; $j++) {
    if ($j -lt $sceneInfo.Count) {
        $finalNarration += [pscustomobject]@{
            chapter = $sceneInfo[$j].chapter
            scene = $sceneInfo[$j].scene
            title = $sceneInfo[$j].title
            duration = $sceneInfo[$j].duration
            narration = $allNarration[$j].narration
            word_count = $allNarration[$j].word_count
        }
    }
}

$output = 'MISTÉRIOS DA CIÊNCIA E DO ESPAÇO`nDocumentário de 90 minutos - Roteiro Completo`n' + ('=' * 60) + '`n`n'
foreach ($item in $finalNarration) {
    $output += '[CAPÍTULO {0} - CENA {1}] {2}`n' -f $item.chapter, $item.scene, $item.title
    $output += 'Duração: {0}s | Palavras: {1}`n' -f $item.duration, $item.word_count
    $output += '{0}`n`n' -f $item.narration
}

Set-Content -Path 'full_narration.txt' -Value $output -Encoding UTF8

Write-Host "Total scenes: $($finalNarration.Count)"
Write-Host "Total words: $totalWords"
Write-Host "Average words per minute: $([math]::Round($totalWords / 90, 1))"
Write-Host "Target words per minute: 125"
Write-Host "Expected duration at 125 wpm: $([math]::Round($totalWords / 125, 1)) minutes"