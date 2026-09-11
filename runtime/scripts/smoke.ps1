$ErrorActionPreference = "Stop"

$project = $args[0]
if (-not $project) {
  $project = (Get-Location).Path
}

aeos init $project
aeos doctor $project
aeos scan $project
aeos gates plan $project
aeos audit $project
aeos provider status $project
aeos context pack $project
aeos status $project
