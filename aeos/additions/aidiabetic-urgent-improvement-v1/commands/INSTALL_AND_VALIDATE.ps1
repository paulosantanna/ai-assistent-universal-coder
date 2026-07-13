param(
  [Parameter(Mandatory=$true)][string]$AeosRoot,
  [Parameter(Mandatory=$true)][string]$TargetRoot
)

$ErrorActionPreference = "Stop"
$PackRoot = Split-Path -Parent $PSScriptRoot

py -3 "$PackRoot\scripts\validate_package.py"
if ($LASTEXITCODE -ne 0) { throw "Pack validation failed" }

py -3 -m pytest "$PackRoot\tests" -ra
if ($LASTEXITCODE -ne 0) { throw "Pack tests failed" }

py -3 "$PackRoot\scripts\install_overlay.py" `
  --aeos-root "$AeosRoot" `
  --target-root "$TargetRoot"

Write-Host "Installed and validated."
