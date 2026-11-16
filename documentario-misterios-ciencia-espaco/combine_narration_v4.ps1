$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

Add-Type -AssemblyName System.Web.Extensions

$allNarration = @()
$totalWords = 0

$serializer = New-Object System.Web.Script.Serialization.JavaScriptSerializer
$serializer.MaxJsonLength = 2147483647

for ($i = 1; $i -le 9; $i++) {
    $filename = '{0:D2}_scenes_chapter{1}.json' -f ($i+2), $i
    $jsonText = Get-Content $filename -Raw -Encoding UTF8
    
    try {
        $data = $serializer.DeserializeObject($jsonText)
        foreach ($scene in $data.scenes) {
            $narration = $scene.narration
            $words = ($narration -split '\s+').Count
            $totalWords += $words
            $allNarration += [pscustomobject]@{
                chapter = $scene.chapter
                scene = $scene.scene
                title = $scene.title
                duration = $scene.duration_seconds
                narration = $narration
                word_count = $words
            }
        }
    }
    catch {
        Write-Host ("Error parsing {0}: {1}" -f $filename, $_.Exception.Message)
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