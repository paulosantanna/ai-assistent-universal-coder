$ErrorActionPreference = "Stop"
$project = $args[0]
if (-not $project) { $project = (Get-Location).Path }
aeos init $project
aeos status $project
aeos plan "Smoke test AEOS runtime" $project
aeos checkpoint "Smoke checkpoint" $project
aeos evidence "Smoke evidence registered" "command" "scripts/test-smoke.ps1" $project
