# SUBAGENT_ORCHESTRATION.md

> **AEOS Chief/Staff Edition**
>
> This document is part of the AI Engineering Operating System.
> It is designed for AI agents acting as Chief AI Architect, Chief Software Architect,
> Principal Engineer, Staff Software Engineer and Staff AI Engineer.
>
> Core invariants:
> - Evidence before claims.
> - Architecture before implementation.
> - Delegation before context bloat.
> - Verification before completion.
> - Knowledge persistence after every material outcome.
> - Human authority over unsafe or high-impact decisions.


## Purpose

Define how AEOS creates, supervises and integrates expert subagents.

## Delegation decision

Delegate when:
- domain expertise improves quality;
- context would bloat ROOT;
- parallelism is safe;
- independent review is needed;
- implementation scope is bounded;
- security or clinical risk exists.

## Subagent contract

Every subagent receives:

```json
{
  "role": "string",
  "staff_level_expectation": true,
  "objective": "string",
  "scope": "string",
  "context": [],
  "constraints": [],
  "allowed_actions": [],
  "forbidden_actions": [],
  "evidence_requirements": [],
  "output_format": "structured_report",
  "escalation_rules": []
}
```

## Required subagent output

```json
{
  "status": "done|blocked|needs_review|rejected",
  "summary": "string",
  "evidence": [],
  "files_read": [],
  "commands_run": [],
  "changes_made": [],
  "risks": [],
  "open_questions": [],
  "lessons": [],
  "recommendation": "accept|rework|escalate"
}
```

## Specialist families

- Architecture specialists
- Language specialists
- Framework specialists
- Security specialists
- Testing specialists
- Performance specialists
- Data/AI specialists
- DevOps specialists
- Clinical/regulatory specialists
- Documentation specialists

## ROOT integration rule

The ROOT Agent integrates results but must not silently overwrite specialist warnings.

Every unresolved warning must be accepted, rejected with evidence, or escalated.
