$ErrorActionPreference = 'Stop'

$envFile = Join-Path $PSScriptRoot '..\.env.local'
if (-not (Test-Path -LiteralPath $envFile)) {
    function New-LocalSecret { [Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(48)) }
    $entries = [ordered]@{
        REIDOABC_PORT = '8088'
        REIDOABC_DB_NAME = 'reidoabc_local'
        REIDOABC_DB_USER = 'reidoabc_local'
        REIDOABC_DB_PASSWORD = New-LocalSecret
        REIDOABC_DB_ROOT_PASSWORD = New-LocalSecret
        REIDOABC_LOCAL_ADMIN_PASSWORD = New-LocalSecret
        REIDOABC_AUTH_KEY = New-LocalSecret
        REIDOABC_SECURE_AUTH_KEY = New-LocalSecret
        REIDOABC_LOGGED_IN_KEY = New-LocalSecret
        REIDOABC_NONCE_KEY = New-LocalSecret
        REIDOABC_AUTH_SALT = New-LocalSecret
        REIDOABC_SECURE_AUTH_SALT = New-LocalSecret
        REIDOABC_LOGGED_IN_SALT = New-LocalSecret
        REIDOABC_NONCE_SALT = New-LocalSecret
    }
    ($entries.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }) | Set-Content -LiteralPath $envFile
}

docker compose --env-file .env.local up --build -d
if ($LASTEXITCODE -ne 0) { throw 'Docker Compose could not start the local runtime.' }
Write-Output 'Local WordPress runtime started at http://localhost:8088/'
