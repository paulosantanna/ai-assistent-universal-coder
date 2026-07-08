# AEOS Runtime MVP v1

Minimal local runtime for the **AEOS Chief/Staff Edition**.

This runtime is intentionally small. It does not try to be an autonomous agent yet. Its job is to provide the first executable kernel for loading an AEOS project, creating runtime state, creating task plans, storing checkpoints, registering evidence, and running a basic judge pass.

## Requirements

- Node.js 20+
- npm

## Install

Extract this folder into:

```text
E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1\runtime
```

Then run:

```powershell
cd E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1\runtime
npm install
npm run build
npm link
```

After `npm link`, the `aeos` command should be available locally.

## Commands

```powershell
aeos help
aeos init E:\GitHub\aidiabetic-research
aeos status E:\GitHub\aidiabetic-research
aeos plan "Audit repository architecture and produce remediation plan" E:\GitHub\aidiabetic-research
aeos checkpoint "Initial runtime checkpoint" E:\GitHub\aidiabetic-research
aeos evidence "AGENT.md exists" "config" ".aeos/AGENT.md" E:\GitHub\aidiabetic-research
aeos judge <TASK_ID> E:\GitHub\aidiabetic-research
```

## Runtime files

Inside the target project, AEOS creates:

```text
.aeos-runtime/
├── tasks/
├── checkpoints/
├── memory/
│   └── memory.jsonl
├── evidence/
│   └── evidence.jsonl
└── runtime-state.json
```

## What this MVP does not do yet

- It does not call LLM APIs.
- It does not edit repository code.
- It does not spawn real subagents.
- It does not run build/test commands automatically.
- It does not implement distributed scheduling.
