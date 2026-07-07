# KNOWLEDGE_ENGINE.md

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

Transform raw work into reusable organizational knowledge.

## Knowledge pipeline

```text
Observation → Evidence → Finding → Lesson → Validated Lesson → Golden Knowledge → Principle
```

## Promotion rules

Observation becomes Evidence only after verification.
Evidence becomes Finding only after interpretation.
Finding becomes Lesson only if reusable.
Lesson becomes Validated Lesson after repeated confirmation.
Validated Lesson becomes Golden Knowledge after high confidence.
Golden Knowledge becomes Principle only if broadly applicable.

## Knowledge record

```json
{
  "id": "uuid",
  "type": "observation|evidence|finding|lesson|validated_lesson|golden_knowledge|principle",
  "summary": "string",
  "context": "string",
  "evidence": [],
  "confidence": "low|medium|high",
  "created_at": "iso-8601",
  "review_required": true
}
```

## Rule

Memory must reduce future mistakes, not accumulate noise.
