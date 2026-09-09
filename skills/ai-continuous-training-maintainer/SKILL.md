# AI Continuous Training Maintainer

Governance: CodENavi Full Workspace v2
Version: 3.0.0
Risk: HIGH

## Mission

Maintain AI continuous-training pipelines with evidence-backed dependency, security, data-governance, evaluation and operational improvements while preserving reproducibility and preventing unreviewed model or data regressions.

This is a skill executed by `codenavi-agent`; it creates no additional agent identity.

## Activation

Activate for requests to audit, repair or evolve continuous-training pipelines, including:

- model/data training pipeline maintenance;
- dependency and CVE review;
- SAST/container/security checks;
- training-loop reliability;
- reproducibility and provenance;
- evaluation-gate maintenance;
- controlled dependency upgrades;
- drift or regression investigation;
- governed continuous-learning workflows.

## Non-goals

Do not:

- mutate production or training infrastructure without explicit authority;
- auto-promote model weights, datasets or learned knowledge without validation;
- invent scan results, CVEs, benchmarks or passing tests;
- expose credentials, tokens, dataset secrets or protected health information;
- change unrelated application code;
- treat model confidence as evidence.

## Inputs

Required:

- target repository or authorized source scope;
- concrete maintenance objective.

Conditionally required:

- current dependency manifests/lockfiles;
- training/evaluation configuration;
- dataset lineage metadata;
- current scan/test output;
- official/current framework documentation when behavior is version-sensitive.

## Workflow

Follow `BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF`.

### BRIEFING

Define target pipeline, desired state, non-goals, risk, allowed mutation scope and success criteria.

### RECON

Inspect `.notebook/INDEX.md`, repository configuration, dependency manifests, training/evaluation code, current evidence and relevant official documentation. Establish the current state before proposing a change.

### PLAN

Prefer the smallest safe change. For dependency or framework changes, identify compatibility boundaries, migration notes, rollback and verification before editing.

### EXECUTE

Apply only authorized changes. Preserve data lineage, deterministic configuration, seeds where applicable, dependency locking and existing project conventions. AEOS orchestration remains Node.js/TypeScript even when the target training project is Python.

### VERIFY

Use applicable deterministic checks:

- unit/integration tests;
- static analysis;
- dependency audit;
- schema/config validation;
- container scan;
- training smoke test;
- evaluation regression checks;
- reproducibility/provenance validation.

Never claim a check passed unless it ran and evidence is available.

### DEBRIEF

Report changed files, evidence, unresolved risks, rollback information and any intentionally deferred work. Update `.notebook/` only with validated reusable project facts.

## Security and governance

- Runtime-only secrets; redact sensitive values from output and evidence.
- Use current vulnerability sources and project versions; do not infer package safety from model memory.
- Treat training data and model artifacts as governed supply-chain inputs with provenance.
- High-impact mutations require existing AEOS policy/permission/approval/rollback gates.
- Judge is an independent deterministic runtime gate/service for governed completion; it is not emitted as a persona artifact.

## Dependency policy

Before upgrading a package:

1. identify current and target versions;
2. read project constraints and authoritative release/security notes;
3. identify breaking changes and transitive impact;
4. update the minimum necessary manifests/code;
5. refresh lockfiles through the authorized toolchain;
6. run affected tests/scans;
7. record rollback and residual risk.

## Model/data change policy

For changes affecting training data, objectives, adapters, checkpoints or evaluation:

- preserve baseline evidence;
- define measurable acceptance criteria before mutation;
- compare against the baseline using the same evaluation protocol;
- block promotion on material unexplained regression;
- preserve provenance for datasets, code, config and model artifacts;
- require explicit human authorization for production promotion when configured by workspace policy.

## Completion criteria

Complete only when:

- scope and evidence are explicit;
- authorized changes are minimal and reviewable;
- applicable tests/scans/evals have passed or blockers are reported;
- no secret/sensitive data is exposed;
- rollback is defined for risky changes;
- no additional agent identity or delegation model was introduced;
- workspace governance guards remain green.
