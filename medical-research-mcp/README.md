# Medical Research MCP

A complete AEOS MCP, playbook, engineering skill, subagent system, and strict validator for evolving an existing disease-focused medical AI repository into a governed research-only Beta.

## Structure

```text
medical-research-mcp/
├── src/medical_research_mcp/
│   ├── server.py
│   ├── AI_architecture.py
│   ├── AI_architecture_best_practices.py
│   ├── AI_trainning_pipeline.py
│   ├── AI_OWASP.py
│   ├── AI_best_practises.py
│   ├── python_best_practises.py
│   ├── repository.py
│   ├── research.py
│   ├── continuos_learning.py
│   ├── continuos_learning_architecture.py
│   ├── RAG.py
│   ├── lora_qora_dora_doubleLora.py
│   ├── bm25.py
│   ├── expert_validator(accepts only with 10.0).py
│   ├── subagents.py
│   ├── qulified_sites_for_medical_researchs_around_world.py
│   ├── audit.py
│   ├── planning.py
│   └── models.py
├── playbooks/
│   └── MEDICAL_AI_COMPLETE_PLAYBOOK.md
├── skills/
│   └── medical-ai-engineering/
│       ├── SKILL.md
│       ├── handover/
│       ├── knowledge/
│       ├── learning/
│       ├── subagents/
│       └── memory/
├── config/
│   ├── disease-profile.yaml
│   └── mcp-server.json
├── schemas/
│   └── evidence.schema.json
├── docs/
│   ├── ARCHITECTURE.md
│   └── REGULATORY_AND_SCIENTIFIC_BOUNDARIES.md
├── tests/
├── scripts/
│   └── validate_package.py
├── pyproject.toml
├── SOURCES.md
└── README.md
```

Additional support modules include dependency intelligence, token budgets, importable aliases, and an importable strict validator.

## Install

```powershell
cd E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1\medical-research-mcp
py -3 -m pip install -e ".[dev]"
```

## Validate package

```powershell
py -3 .\scripts\validate_package.py
```

## Run tests

```powershell
py -3 -m pytest -ra
```

## Start MCP

```powershell
py -3 -m medical_research_mcp.server
```

## Audit the existing project

```powershell
py -3 -m medical_research_mcp.audit "E:\GitHub\aidiabetic-research"
```

## MCP configuration

Copy or merge `config/mcp-server.json` into the MCP client configuration. Replace `${workspaceFolder}` when the client does not expand it.

## Main tools

- repository scanning and architecture inventory;
- repository audit;
- architecture recommendation;
- training-pipeline design and audit;
- OWASP AI gate;
- RAG and continuous-learning gates;
- BM25 baseline;
- LoRA/QLoRA/DoRA recommendation;
- PubMed, Europe PMC, and ClinicalTrials.gov research;
- qualified-source registry;
- dependency inventory;
- OSV, CISA KEV, and EPSS queries;
- specialized-subagent registry;
- token-budget planning;
- complete Beta plan;
- strict expert validation.

## Strict 10.0 rule

The Judge does not manufacture a score.

Acceptance requires every mandatory criterion to pass with direct evidence and a computed score of exactly `10.0`. Otherwise the result is `REWORK_REQUIRED`.

## Scientific boundary

This system may organize evidence and generate computational hypotheses. It cannot autonomously authorize laboratory, animal, or human experimentation and cannot establish a cure.
