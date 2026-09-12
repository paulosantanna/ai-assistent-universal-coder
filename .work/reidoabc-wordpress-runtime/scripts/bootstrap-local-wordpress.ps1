$ErrorActionPreference = 'Stop'

$envPath = Join-Path $PSScriptRoot '..\.env.local'
if (-not (Test-Path -LiteralPath $envPath)) { throw 'Run scripts/start-local.ps1 first.' }
$entries = @{}
Get-Content -LiteralPath $envPath | ForEach-Object { if ($_ -match '^([^=]+)=(.*)$') { $entries[$matches[1]] = $matches[2] } }
$adminPassword = $entries['REIDOABC_LOCAL_ADMIN_PASSWORD']
if ([string]::IsNullOrWhiteSpace($adminPassword)) { throw 'Local admin password is missing from .env.local.' }

docker compose --env-file .env.local exec -T -e REIDOABC_BOOTSTRAP_ADMIN_PASSWORD=$adminPassword wordpress php /var/www/html/scripts/local-bootstrap.php
if ($LASTEXITCODE -ne 0) { throw 'WordPress bootstrap failed.' }

Write-Output 'Database, WooCommerce, account flow and catalog are ready at http://localhost:8088/'
Write-Output 'The local administrator is reidoabc_admin; its password is stored only in .env.local.'
