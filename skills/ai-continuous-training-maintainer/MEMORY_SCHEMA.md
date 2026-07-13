# MEMORY_SCHEMA.md
# AI Continuous Training Maintainer — Memory Schema

## 1. Purpose

Define the mandatory structure, lifecycle, authority and integrity rules for memory within this skill.

## 2. Memory classes

### 2.1 Execution memory
Produced by: CHILD agents
Location: `memory/children/executions/<execution-id>/`
Content: HANDOFF.md, EXECUTION_LOG.md, EVIDENCE_INDEX.md, RESULT.md, DIFF.patch
Trust: RAW_EVIDENCE

### 2.2 Domain candidate memory
Produced by: PARENT agents
Location: `memory/parents/<domain>/`
Content: DOMAIN_CONTEXT.md, LESSONS.md, FAILURES.md, PATTERNS.md
Trust: CANDIDATE

### 2.3 Root memory
Produced by: ROOT Agent
Location: `memory/root/`
Content: strategic lessons, cross-domain dependencies, systemic failures
Trust: REVIEWED

### 2.4 Shared institutional memory
Location: `memory/shared/`
Contains only reviewed and promoted knowledge
Trust: VALIDATED

## 3. Memory-write restrictions

- CHILD writes only to `memory/children/executions/<execution-id>/`
- PARENT writes only to `memory/parents/<domain>/`
- ROOT writes only to `memory/root/`
- Quality-Judge appends score reports
- Shared memory: read-only for all agents (written by Knowledge Curator)

## 4. Entry schema

Every entry must have:
- id (UUID)
- timestamp (ISO 8601)
- source (agent role + execution_id)
- content (structured per class)
- evidence_refs (list of evidence)
- validation_status (RAW | CANDIDATE | REVIEWED | VALIDATED | DEPRECATED)

## 5. Integrity

- Memory without provenance is invalid
- Memory without evidence is UNVERIFIED
- Snapshots are SHA-256 verified before and after storage
- No secrets may be stored in any memory class

## 6. Directory structure

```
memory/
├── EXECUTIONS.md          — consolidated execution log (all iterations)
├── LESSONS.md             — cross-domain lessons
├── FAILURES.md            — consolidated failures
├── PATTERNS.md            — identified patterns
├── root/                  — ROOT Agent memory
├── parents/
│   └── <domain>/          — PARENT Agent domain memory
├── children/
│   └── executions/
│       └── <execution-id>/ — CHILD execution memory
└── shared/                — promoted institutional knowledge
```
