# Token Economy Policy

## Goal

Maximize useful engineering output per token while preserving evidence and root-cause fidelity across DeepSeek, GPT-5-class, Gemini-class, local and future models.

## Never enter model context

- PAT/token/Authorization header/cookies;
- secret values or credential-helper output;
- complete successful workflow logs;
- full Git history;
- binary artifacts;
- datasets/models/embeddings;
- unrelated repository files.

## Evidence packet pipeline

`raw log -> secret redaction -> success-noise removal -> failing-step extraction -> normalized stack/error -> fingerprint -> changed-file correlation -> relevant excerpts -> evidence refs`.

## Cache keys

Cache immutable analysis by:

- head SHA;
- workflow/job ID + attempt;
- file SHA-256;
- failure fingerprint;
- architecture summary version.

Invalidation: any changed input hash or new head SHA invalidates dependent cache entries.

## Budgets

```yaml
global_recovery_budget: 240000
per_cycle_budget: 40000
per_root_cause_budget: 14000
workflow_guardian_budget: 3000
job_guardian_budget: 1500
specialist_lens_budget: 10000
judge_budget: 10000
```

A guardian normally consumes only state metadata. Deep context is loaded only for an active failure.

## Model routing by capability

Use configured capability profiles rather than hard-coded vendor/model names. Suggested preference:

- simple workflow YAML / focused deterministic failure: low-cost coding model;
- dependency/test repair: low-cost coding model, escalate if cross-module;
- complex architectural regression: strongest reasoning model;
- security-sensitive review: strongest security/reasoning profile;
- very large monorepo or multi-workflow correlation: large-context profile;
- Judge: deterministic gates first, model assistance only as non-authoritative review.

## No-progress economy

When the same fingerprint repeats twice without new evidence, stop rather than spend more tokens. Do not reread unchanged files or resend identical logs.
