# AEOS Memory Governance

## Purpose

Memory must improve execution without becoming an uncontrolled data sink.

## Memory Types

```text
semantic
architectural
procedural
episodic
operational
lessons_learned
do
dont
```

## Memory Gateway

All memory reads/writes must pass through MemoryGateway.

## Write Rules

A memory write requires:

- execution_id
- source evidence
- producing agent
- memory type
- confidence
- expiry policy if applicable
- security classification

## Forbidden Memory

Never persist:

- secrets;
- tokens;
- cookies;
- API keys;
- passwords;
- private keys;
- browser sessions;
- raw credentials;
- unredacted logs.

## Lessons Learned Format

```yaml
lesson:
  id:
  source_execution_id:
  problem:
  root_cause:
  impact:
  correction:
  prevention:
  evidence_refs:
  applies_to:
```
