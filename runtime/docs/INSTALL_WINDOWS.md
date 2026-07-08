# Install AEOS Runtime Core v9.1 on Windows

```powershell
cd E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1

if (Test-Path runtime) {
    Remove-Item runtime -Recurse -Force
}

Expand-Archive -Path "C:\Users\paulo\Downloads\AEOS_RUNTIME_CORE_v9_1.zip" -DestinationPath "E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1" -Force
Rename-Item AEOS_RUNTIME_CORE_v9_1 runtime

cd runtime
npm install
npm run build
npm link
aeos help
```
