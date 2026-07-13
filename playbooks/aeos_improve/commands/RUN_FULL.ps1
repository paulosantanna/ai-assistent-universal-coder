param(
  [Parameter(Mandatory=$true)][string]$AeosRoot,
  [Parameter(Mandatory=$true)][string]$TargetRoot,
  [ValidateSet("controlled","dry-run")][string]$Mode = "controlled"
)

$ErrorActionPreference = "Stop"
$PackId = "aidiabetic-urgent-improvement-v1"

if (-not (Test-Path -LiteralPath $AeosRoot -PathType Container)) {
  throw "AEOS root not found: $AeosRoot"
}
if (-not (Test-Path -LiteralPath $TargetRoot -PathType Container)) {
  throw "Target root not found: $TargetRoot"
}

Push-Location $AeosRoot
try {
  $aeosCmd = Get-Command aeos -ErrorAction SilentlyContinue
  if (-not $aeosCmd) {
    Write-Host "AEOS CLI not found on PATH." -ForegroundColor Yellow
    Write-Host "Use FULL_EXECUTION_PROMPT.md with the installed agent runtime."
    exit 2
  }

  $argsList = @("playbook", "run", $PackId, "--target", $TargetRoot)
  if ($Mode -eq "dry-run") { $argsList += "--dry-run" }

  Write-Host ("Executing: aeos " + ($argsList -join " "))
  & aeos @argsList
  $code = $LASTEXITCODE
  if ($code -ne 0) {
    Write-Host "The installed AEOS CLI may use a different playbook syntax." -ForegroundColor Yellow
    Write-Host "Equivalent objective: run '$PackId' against '$TargetRoot'."
    Write-Host "Fallback contract: FULL_EXECUTION_PROMPT.md"
  }
  exit $code
}
finally {
  Pop-Location
}
