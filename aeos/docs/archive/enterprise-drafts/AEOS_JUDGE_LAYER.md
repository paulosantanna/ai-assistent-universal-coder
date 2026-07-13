# AEOS Judge Layer

## Purpose

The Judge Layer validates whether an execution can be accepted.

## Judge Types

```text
Deterministic Judge
  Validates objective facts, evidence, hashes, tests, approvals, policies.

LLM Judge
  Optional future layer for qualitative review.
```

## Absolute Rule

LLM Judge can never override Deterministic Judge failure.

## Automatic BLOCKED Conditions

- missing evidence;
- hash mismatch;
- secret exposure;
- missing rollback;
- failed required test;
- missing approval;
- protected branch mutation;
- direct tool bypass;
- package verification failure;
- unregistered skill/playbook;
- unsupported claim without evidence.
