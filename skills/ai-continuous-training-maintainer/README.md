# AI Continuous Training Maintainer

Skill MCP-connected para manter o pipeline de treino contínuo de IA em `E:/GitHub/aidiabetic-research/src/` sempre atualizado com melhores práticas, CVEs resolvidas, SAST aprovado e dependências seguras.

## Arquitetura

```
┌──────────────────────────────────────┐
│        SKILL: ai-continuous-         │
│        training-maintainer           │
│                                      │
│  ┌────────────────────────────────┐  │
│  │      5 Subagentes              │  │
│  │  ┌──────┐ ┌──────┐ ┌──────┐   │  │
│  │  │ CVE  │ │ SAST │ │ Libs │   │  │
│  │  │Resolver│Analyzer│Updater│   │  │
│  │  └──────┘ └──────┘ └──────┘   │  │
│  │  ┌──────┐ ┌──────┐           │  │
│  │  │ Code │ │Rollb.│           │  │
│  │  │Quality│Snapshot│          │  │
│  │  └──────┘ └──────┘           │  │
│  └────────────────────────────────┘  │
│                                      │
│  ┌────────────────────────────────┐  │
│  │ Memory & Knowledge            │  │
│  │ - EXECUTIONS, LESSONS,        │  │
│  │   FAILURES, PATTERNS          │  │
│  │ - POSITIVE/NEGATIVE knowledge │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

## Ativação

```
/ai-continuous-training-maintainer <comando>
```

Comandos: `update`, `cve`, `sast`, `deps`, `rollback`, `health`

## Dependências

- Python 3.11+
- pip-audit, bandit, ruff, mypy, pytest
- Trivy (opcional para scan de container/filesystem)
- Git
