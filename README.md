# AEOS Chief/Staff Edition

AI Engineering Operating System — Chief/Staff Edition.

AEOS is a specification-first operating system for AI agents. It treats the LLM as a reasoning component inside a governed engineering runtime, not as the entire system.

## Objective

Build an AI operating system capable of orchestrating software engineering, AI engineering, research, verification, governance, continuous learning and specialist agent execution with Staff/Chief-level discipline.

## Core architecture

```mermaid
flowchart TD
    U[User Request] --> K[AEOS Kernel / ROOT Agent]
    K --> H[N-Layer Hierarchy]
    K --> O[Organization Model]
    K --> X[Execution Engine]
    X --> P[Planning Engine]
    P --> D[Task Decomposition]
    D --> S[Subagent Orchestration]
    S --> A[Specialist Agents]
    A --> E[Evidence Engine]
    E --> J[Judge Engine]
    J --> C[Consensus Engine]
    C --> M[Memory / Knowledge System]
    C --> R[Final Result]
```

## Included modules

- Foundation: constitution, hierarchy, organization, principles.
- Execution: planning, decomposition, orchestration, checkpoints, deep thinking.
- Reasoning: evidence, meta-reasoning, failure prediction, architecture reasoning, trade-offs, research.
- Knowledge: memory, lessons, golden knowledge, ADRs, continuous learning.
- Engineering: language discovery, language standards, architecture patterns, Clean Architecture, DDD, AI, security, observability.
- Verification: quality gates, testing, judge engine, consensus, scoring, release.
- Governance: clinical, regulatory, risk, security governance, human-in-the-loop.
- Operations: commands, playbook, self-improvement, runtime.
- Protocols, schemas, templates and examples.

## Installation

Recommended repository layout:

```text
.aeos/
├── AGENT.md
├── foundation/
├── execution/
├── reasoning/
├── knowledge/
├── engineering/
├── verification/
├── governance/
├── operations/
├── protocols/
├── schemas/
├── templates/
└── examples/
```

Point your AI coding agent to `.aeos/AGENT.md`.

## Operating posture

The ROOT Agent is not a naive coder. It is the AI kernel and Chief/Staff orchestrator of the engineering organization.
