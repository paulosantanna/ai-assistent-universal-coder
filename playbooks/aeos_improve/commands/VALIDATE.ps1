$ErrorActionPreference = "Stop"
$PackRoot = Split-Path -Parent $PSScriptRoot
py -3 "$PackRoot\scripts\validate_package.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
py -3 -m pytest "$PackRoot\tests" -ra
exit $LASTEXITCODE
