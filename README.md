# AEOS Hierarchical Agent System

This package contains the revised AEOS hierarchy and governed learning contracts.

## Included files

- `AGENT.md`
- `ROOT_AGENT.md`
- `PARENT_AGENT.md`
- `CHILD_AGENT.md`
- `HANDOFF.md`
- `MEMORY_SCHEMA.md`
- `KNOWLEDGE_PROMOTION.md`
- `CONTINUOUS_LEARNING.md`

## Recommended installation

```text
AEOS/
├── AGENT.md
├── agents/
│   ├── ROOT_AGENT.md
│   ├── PARENT_AGENT.md
│   └── CHILD_AGENT.md
├── learning/
│   ├── HANDOFF.md
│   ├── MEMORY_SCHEMA.md
│   ├── KNOWLEDGE_PROMOTION.md
│   └── CONTINUOUS_LEARNING.md
└── memory/
    ├── root/
    ├── parents/
    ├── children/executions/
    └── shared/
```

Adjust the bootstrap paths in `AGENT.md` if the files are moved into subdirectories.

## Core design

- Three execution levels: Root, Parent and Child.
- Four operational layers: deep understanding, negative knowledge, validated positive knowledge and continuous learning.
- Explicit handoffs for every responsibility transfer.
- Child memory remains execution-local.
- Parent and Root write candidate memory.
- Only governed promotion creates shared institutional knowledge.
