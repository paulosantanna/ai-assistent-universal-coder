# AEOS Runtime Core v9.1

Runtime Core v9.1 keeps AEOS focused on deterministic workspace operations: scan, gates, audit, evidence, memory, context packs, runbooks, release checks and delivery artifacts.

## AI Provider Policy

AI providers are disabled for this workspace.

Blocked surfaces include:

- Ollama.
- Hosted LLM APIs.
- DeepSeek-compatible APIs.
- OpenAI-compatible local or remote gateways.
- OpenCode model gateways.
- Provider templates that would re-enable model access.

The runtime must not configure providers, list provider models, call model inference endpoints, or create provider templates. `aeos provider status` is kept only as a diagnostic command and reports the disabled state.

## Stable Commands

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

aeos provider status
aeos agent runs
aeos agent latest

aeos prompt audit
aeos prompt fix
aeos prompt migration
aeos subagents plan
aeos adr create
aeos lessons add

aeos context pack
aeos remediate plan
aeos backlog generate

aeos workflow audit
aeos workflow fix
aeos runbook generate
aeos policy generate
aeos ci github
aeos release check

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
cd E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1\runtime
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

## Recommended Flow

```powershell
aeos init E:\GitHub\aidiabetic-research
aeos audit run-gates E:\GitHub\aidiabetic-research
aeos context pack E:\GitHub\aidiabetic-research
aeos provider status E:\GitHub\aidiabetic-research
aeos status E:\GitHub\aidiabetic-research
```

## Outputs

```text
.aeos-runtime/
├── evidence/
├── gates/
├── reports/
├── context/
├── runbooks/
├── delivery/
└── ...
```
