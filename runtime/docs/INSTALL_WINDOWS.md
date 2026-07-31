# Install AEOS Runtime Core on Windows

This guide installs the AEOS CLI from the local repository.

The expected result is:

```powershell
aeos help
```

showing the AEOS command list.

## Requirements

- Windows 10 or Windows 11.
- PowerShell 7+ recommended.
- Git installed and available in `PATH`.
- Node.js 20 LTS or newer.
- npm available in `PATH`.
- Optional: Ollama, only if you want to run local agent execution commands.

Check the basics:

```powershell
git --version
node --version
npm --version
```

## Install from Git

Use this path when the repository is available in GitHub.

```powershell
cd E:\GitHub
git clone https://github.com/paulosantanna/ai-assistent-universal-coder.git
cd .\ai-assistent-universal-coder\runtime

npm install
npm run build
npm link
aeos help
```

## Install from an existing local checkout

Use this path when the repository already exists on your machine.

```powershell
cd E:\GitHub\ai-assistent-universal-coder\runtime

npm install
npm run build
npm link
aeos help
```

## Install from a ZIP package

Use this path when the project was downloaded as a ZIP.

```powershell
cd E:\GitHub
Expand-Archive -Path "$env:USERPROFILE\Downloads\ai-assistent-universal-coder.zip" -DestinationPath "E:\GitHub" -Force
cd .\ai-assistent-universal-coder\runtime

npm install
npm run build
npm link
aeos help
```

If the ZIP extracts to a folder with a suffix such as `-main`, adjust the `cd` command:

```powershell
cd E:\GitHub\ai-assistent-universal-coder-main\runtime
```

## One-command local installer

From the `runtime` folder:

```powershell
.\scripts\install-local.ps1
```

The script runs:

```powershell
npm install
npm run build
npm link
aeos help
```

## Validate the installation

Run:

```powershell
aeos help
aeos doctor E:\GitHub\ai-assistent-universal-coder
aeos scan E:\GitHub\ai-assistent-universal-coder
```

For a target project:

```powershell
aeos init E:\GitHub\aidiabetic-research
aeos audit run-gates E:\GitHub\aidiabetic-research
aeos context pack E:\GitHub\aidiabetic-research
```

## Optional Ollama setup

Install Ollama and start it locally, then configure AEOS:

```powershell
aeos provider configure ollama http://localhost:11434 llama3.1 E:\GitHub\aidiabetic-research
aeos provider status E:\GitHub\aidiabetic-research
aeos provider models E:\GitHub\aidiabetic-research
```

Replace `llama3.1` with the model installed on your machine, for example:

```powershell
aeos agent run audit ollama qwen2.5-coder E:\GitHub\aidiabetic-research
aeos agent latest E:\GitHub\aidiabetic-research
```

## Optional DeepSeek and OpenAI-compatible providers

Hosted providers should be configured through environment variables. AEOS stores
the environment variable name, not the secret value.

DeepSeek-compatible:

```powershell
$env:DEEPSEEK_API_KEY = "<token from your environment>"
aeos provider configure deepseek deepseek-chat DEEPSEEK_API_KEY E:\GitHub\aidiabetic-research
aeos agent run audit deepseek deepseek-chat E:\GitHub\aidiabetic-research
```

Local OpenAI-compatible server such as LM Studio or llama.cpp:

```powershell
aeos provider configure openai-compatible http://localhost:1234/v1 local-model "" E:\GitHub\aidiabetic-research
aeos agent run audit openai-compatible local-model E:\GitHub\aidiabetic-research
```

OpenCode with the same local or gateway model:

```powershell
aeos provider template opencode E:\GitHub\aidiabetic-research
aeos provider configure opencode http://127.0.0.1:1234/v1 local-model "" E:\GitHub\aidiabetic-research
aeos agent run audit opencode local-model E:\GitHub\aidiabetic-research
```

Use the generated provider template as the base for `opencode.json`. Keep raw
keys out of repository files; use OpenCode auth or environment variables.

## Update an existing installation

```powershell
cd E:\GitHub\ai-assistent-universal-coder
git pull
cd .\runtime

npm install
npm run build
npm link
aeos help
```

## Fix npm link conflicts

If `npm link` reports that `aeos` already exists, remove the previous global link and link again:

```powershell
npm uninstall -g aeos
Remove-Item "$env:APPDATA\npm\aeos" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:APPDATA\npm\aeos.cmd" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:APPDATA\npm\aeos.ps1" -Force -ErrorAction SilentlyContinue
npm link
aeos help
```

## Common problems

### `tsc` or `tsx` not found

Run the install from the `runtime` directory:

```powershell
cd E:\GitHub\ai-assistent-universal-coder\runtime
npm install
npm run build
```

### `aeos` is not recognized

The CLI was built, but not linked globally.

```powershell
cd E:\GitHub\ai-assistent-universal-coder\runtime
npm link
aeos help
```

If the command still fails, close and reopen PowerShell.

### PowerShell blocks the script

Run the installer with a process-local execution policy:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-local.ps1
```

### Build passes but `npm run smoke` fails

`npm run smoke` uses `tsx`. Some restricted or sandboxed environments block the IPC pipe used by `tsx`.

In that case, validate the compiled CLI directly:

```powershell
npm run build
node .\dist\cli\index.js help
```

### Node version issues

Use Node.js 20 LTS or newer. If multiple Node versions are installed, confirm the active one:

```powershell
node --version
npm --version
where node
where npm
```

## Expected runtime output folders

When AEOS runs against a target project, it writes runtime state under:

```text
<target-project>\.aeos-runtime\
```

Typical subfolders:

```text
.aeos-runtime/
  agent-runs/
  providers/
  evidence/
  reports/
```

Do not commit generated runtime folders unless a specific evidence package requires it.
