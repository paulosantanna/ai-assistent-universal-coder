# AEOS Workbench

**Portable AI-First Engineering Environment** — v1.0.0

Governado, orientado a evidências, criado para entender, operar, automatizar, evoluir e auditar ecossistemas de software.

## Architecture

```
workbench/
├── AEOS_CONSTITUTION.md        # Supreme contract
├── AEOS_KERNEL.md              # Kernel spec
├── AEOS_AGENT_CONTRACT.md      # Agent interface
├── AEOS_SKILL_CONTRACT.md      # Skill interface
├── AEOS_PLAYBOOK_CONTRACT.md   # Playbook interface
├── AEOS_POLICY_ENGINE.md       # Policy engine spec
├── AEOS_PERMISSION_MODEL.md    # Permission model
├── AEOS_MEMORY_MODEL.md        # Memory system
├── AEOS_JUDGE_LAYER.md         # Judge evaluation
├── AEOS_SECURITY_MODEL.md      # Security model
├── AEOS_ECOSYSTEM_SCHEMA.md    # Ecosystem schema
├── AEOS_MVP_ROADMAP.md         # Roadmap
├── Core/                       # Kernel, Context, Policy, etc.
├── Ecosystem/                  # Scanner, StackDetector, mappers
├── Env/                        # Docker, Devcontainer, CI generators
├── Agents/                     # Agent specifications by role
├── Skills/                     # Registry, Factory, Evaluator
├── Playbooks/                  # Registry, Executor, Templates
├── Memory/                     # Semantic, Procedural, Episodic...
├── Security/                   # Secrets, Approvals, Redaction
├── Observability/              # Logs, Traces, Metrics
├── CLI/                        # CLI interface
├── Desktop/                    # Desktop interface (future)
├── Config/                     # Configuration
└── Mvp/                        # Python MVP implementation
    ├── pyproject.toml
    └── src/aeos_workbench/
        ├── cli/                # CLI entry point
        ├── scanner/            # Project scanner
        ├── stack_detector/     # Stack detection
        ├── evidence/           # Evidence ledger
        ├── judge/              # Judge engine
        ├── generator/          # Report generators
        └── report/             # Report utilities
```

## Quick Start

```bash
cd workbench/Mvp
pip install -e .
aeos full-scan --path /path/to/project
```

## Core Principles

1. **Evidence First** — No claim without evidence
2. **Human Sovereignty** — Destructive actions require approval
3. **Separation of Powers** — Judge ≠ Implementer
4. **Radical Transparency** — All actions logged
5. **Portability** — Windows, Linux, macOS, Docker, WSL
