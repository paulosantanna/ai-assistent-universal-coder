$ErrorActionPreference = "Stop"
Write-Host "Installing AEOS Runtime MVP locally..."
npm install
npm run build
npm link
Write-Host "Done. Try: aeos help"
