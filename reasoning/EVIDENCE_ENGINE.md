# EVIDENCE_ENGINE.md

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

Ensure every meaningful claim has traceable support.

## Evidence classes

- Code evidence: file path + line range.
- Command evidence: command + exit code + output.
- Test evidence: test name + status + logs.
- Config evidence: file path + value.
- Diff evidence: changed file + patch.
- Source evidence: URL, DOI, standard, documentation.
- Benchmark evidence: method + result + environment.
- Security evidence: scanner + finding + severity.
- Clinical evidence: guideline, publication, protocol.

## Evidence object

```json
{
  "evidence_id": "uuid",
  "claim": "string",
  "type": "code|command|test|config|diff|source|benchmark|security|clinical",
  "reference": "string",
  "verification_method": "string",
  "timestamp": "iso-8601",
  "verified": true,
  "limitations": []
}
```

## Evidence strength

Strong:
- direct execution;
- passing automated tests;
- inspected code lines;
- official documentation;
- reproducible benchmark.

Weak:
- indirect inference;
- comments without tests;
- stale documentation;
- anecdotal claims.

Weak evidence may guide exploration but cannot justify final completion.

## Claim policy

No evidence = no claim.
Partial evidence = partial claim.
Contradictory evidence = escalate.
