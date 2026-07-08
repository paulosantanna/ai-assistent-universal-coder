# AEOS Runtime Core v9.1

Runtime Core v9.1 adds the first **real agent execution layer**.

Until v8, AEOS generated context, prompts, remediation plans, backlogs and release artifacts.
In v9, AEOS can execute an agent run through a local provider.

## Provider support in v9

### Real execution

```text
Ollama local HTTP API
```

### Why Ollama first

- No cloud dependency.
- No API key required.
- No external data transfer by default.
- Safer for private repositories and health/clinical projects.

## New commands

```powershell
aeos provider configure ollama [baseUrl] [model] [projectPath]
aeos provider status [projectPath]
aeos provider models [projectPath]
aeos agent run audit ollama [model] [projectPath]
aeos agent run judge ollama [model] [projectPath]
aeos agent run remediate ollama [model] [projectPath]
aeos agent runs [projectPath]
aeos agent latest [projectPath]
```

## Existing stable commands preserved

```powershell
aeos init
aeos status
aeos doctor
aeos modules
aeos scan
aeos export

aeos gates plan
aeos gates results
aeos gate run
aeos audit
aeos audit run-gates
aeos report latest

aeos prompt audit
aeos prompt fix
aeos prompt migration
aeos subagents plan
aeos adr create
aeos lessons add

aeos bridge opencode
aeos bridge codex
aeos bridge cursor
aeos context pack
aeos remediate plan
aeos backlog generate

aeos workflow audit
aeos workflow fix
aeos runbook generate
aeos policy generate
aeos ci github
aeos release check
aeos provider template openai
aeos provider template anthropic
aeos provider template ollama

aeos plan
aeos tasks
aeos task
aeos checkpoint
aeos checkpoints
aeos evidence add
aeos evidence list
aeos memory add
aeos memory list
aeos judge

aeos snapshot create
aeos checklist generate
aeos delivery package
```

## Install

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
```

If `npm link` reports an existing shim:

```powershell
npm uninstall -g aeos
Remove-Item "C:\Users\paulo\AppData\Roaming\npm\aeos" -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Users\paulo\AppData\Roaming\npm\aeos.cmd" -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Users\paulo\AppData\Roaming\npm\aeos.ps1" -Force -ErrorAction SilentlyContinue
npm link
```

## Recommended v9 flow

```powershell
aeos init E:\GitHub\aidiabetic-research
aeos audit run-gates E:\GitHub\aidiabetic-research
aeos context pack E:\GitHub\aidiabetic-research

aeos provider configure ollama http://localhost:11434 llama3.1 E:\GitHub\aidiabetic-research
aeos provider status E:\GitHub\aidiabetic-research

aeos agent run audit ollama llama3.1 E:\GitHub\aidiabetic-research
aeos agent latest E:\GitHub\aidiabetic-research
```

If your local Ollama model is different, replace `llama3.1` with your installed model.

Examples:

```powershell
aeos agent run audit ollama qwen2.5-coder E:\GitHub\aidiabetic-research
aeos agent run remediate ollama qwen2.5-coder E:\GitHub\aidiabetic-research
aeos agent run judge ollama qwen2.5-coder E:\GitHub\aidiabetic-research
```

## Outputs

```text
.aeos-runtime/
├── agent-runs/
│   └── agent-run-*.json
├── providers/
│   └── provider-config.json
└── ...
```

## Important limitation

v9.1 does not automatically patch source code. It runs the agent, stores the response, and registers evidence. Code mutation should be added only after the agent run + judge layer is stable.


## v9.1 fix

Adds:

```powershell
aeos provider models [projectPath]
```

This calls Ollama `/api/tags` and returns locally available models.
