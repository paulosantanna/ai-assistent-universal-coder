# AEOS Value Playbook

## Objective

AEOS generates value when its capabilities are composed around measurable outcomes. The unit of success is not “number of skills invoked”; it is verified improvement to delivery, quality, risk, cost, reliability, maintainability or knowledge continuity.

## Value equation

For each mission, define value in terms of one or more dimensions:

- **Lead time:** less time from request to verified delivery.
- **Change failure rate:** fewer regressions/failed deployments.
- **MTTR:** faster diagnosis and recovery.
- **Security risk:** fewer exploitable or uncontrolled paths.
- **Performance:** lower latency/resource cost or higher throughput.
- **Maintainability:** lower complexity/coupling and safer change surface.
- **Knowledge continuity:** less rediscovery and tribal knowledge loss.
- **Documentation accuracy:** fewer stale/unknown operating assumptions.
- **Business enablement:** faster integration, channel expansion or feature delivery.

Baseline first whenever the outcome is measurable.

## Composition model

Use this as the default full-workspace chain:

`CodENavi governance`
→ `repository/notebook reconnaissance`
→ `specialist analysis`
→ `Critical Thinking / architecture decision`
→ `minimal implementation`
→ `tests + evals + security/performance checks`
→ `PR review`
→ `documentation`
→ `notebook + validated memory`

Not every mission needs every stage, but skipping a stage should be intentional.

## Playbook A — Onboard an unknown repository

**Goal:** turn an unfamiliar repository into an actionable engineering model.

1. Map using `REPOSITORY_MAPPING.md`.
2. Establish build/test baseline.
3. Generate architecture/development/operations docs.
4. Identify top risks and unknowns.
5. Seed `.notebook` with durable pointers.
6. Produce a prioritized next-action backlog.

**Value:** reduces repeated discovery time and enables safer delegation to agents/engineers.

**Metrics:** time-to-first-safe-change, mapping unknown count, build/test baseline status, documentation coverage of critical flows.

## Playbook B — Modernize a legacy application

**Goal:** upgrade without turning modernization into an uncontrolled rewrite.

1. Map current runtime/dependencies/architecture.
2. Establish behavioral/performance baseline.
3. Use version/domain skills such as `java-version-expert` and dependency analysis.
4. Identify compatibility boundaries and migration sequence.
5. Create ADR for major target-state decisions.
6. Execute incremental slices.
7. Verify behavior/security/performance after each slice.
8. Review PRs and update docs/notebook continuously.

**Value:** lower migration risk, shorter feedback cycles, traceable decisions.

**Metrics:** deprecated dependencies removed, CVEs reduced, build/runtime version progress, regression count, latency/resource deltas.

## Playbook C — Reduce production incidents

**Goal:** convert incidents into permanent reliability knowledge.

1. Reconstruct failure path from evidence.
2. Separate symptom, trigger, contributing factors and root cause.
3. Reproduce safely when possible.
4. Map blast radius/failure propagation.
5. Apply minimal corrective change.
6. Add regression/contract test.
7. Improve observability if the failure was hard to detect.
8. Generate/update troubleshooting/runbook documentation.
9. Record durable gotcha/pattern in `.notebook`.

**Value:** lower MTTR and recurrence.

**Metrics:** MTTR, recurrence rate, detection time, regression coverage.

## Playbook D — Security hardening

**Goal:** reduce realistic attack surface without security theater.

1. Map trust boundaries and privileged flows.
2. Inspect auth/authz, inputs, dependencies, secrets and network exposure.
3. Prioritize by exploitability × impact × reachability.
4. Apply bounded remediation.
5. Run security/evaluator checks.
6. Document controls and residual risk.

**Value:** risk reduction backed by evidence.

**Metrics:** reachable critical/high findings, secret exposure count, dependency risk, privileged-path coverage.

## Playbook E — Performance and cost optimization

**Goal:** improve a measured bottleneck, not optimize by intuition.

1. Capture baseline latency/throughput/error/resource profile.
2. Trace the critical path.
3. Identify causal bottleneck.
4. Change the smallest relevant factor.
5. Remeasure under comparable conditions.
6. Reject changes that move cost/regression elsewhere without acceptable trade-off.
7. Document reproducible evidence.

**Value:** measurable capacity/cost/user-experience improvement.

**Metrics:** p50/p95/p99 latency, throughput, CPU/memory, DB/query latency, error rate, infrastructure cost where available.

## Playbook F — Recover a poorly documented system

**Goal:** replace tribal/stale documentation with evidence-backed operational knowledge.

1. Inventory existing docs and mark contradictions/staleness.
2. Map repository/runtime/deployment.
3. Generate high-value missing docs using `docs-writer`.
4. Validate commands and architecture against implementation.
5. Create notebook pointers for future reconnaissance.
6. Delete/deprecate misleading duplicates.

**Value:** faster onboarding, safer maintenance and less knowledge loss.

**Metrics:** critical undocumented flows, stale-doc defects, onboarding/recon time.

## Playbook G — PR quality gate

**Goal:** make review evidence-driven.

1. Resolve requested behavior and acceptance criteria.
2. Map changed files to architecture/data/security boundaries.
3. Review correctness and regression risk.
4. Verify tests prove behavior rather than implementation details.
5. Check dependency/security/performance/documentation impact.
6. Confirm notebook impact when durable project knowledge changed.
7. Produce actionable findings ordered by severity.

**Value:** fewer escaped defects and better review consistency.

## Playbook H — KingHost/site/commerce operations

**Goal:** analyze or operate authorized hosting/site/commerce environments under governance.

Compose the relevant KingHost secure-connection, site lifecycle, code/data/architecture analysis, web modernization and omnichannel skills.

Rules remain strict:

- credentials are runtime-only;
- use verified provider capabilities;
- no invented/private APIs;
- production mutations require the configured approval/Judge/backup/rollback gates;
- analysis should be read-only by default;
- changes must be verified after execution.

**Value:** safer site operations, architecture visibility, performance improvement and channel integration without bypassing security controls.

## Prioritization model

For a backlog of candidate improvements, score each item using evidence:

`Priority = (Impact × Confidence × RiskReduction) / Effort`

The formula is a decision aid, not an automatic truth. Regulatory/security criticality and hard dependencies can override numerical order.

For each candidate record:

- problem/evidence;
- affected business/technical capability;
- impact;
- confidence;
- effort;
- risk if unchanged;
- dependencies;
- verification metric.

## Avoiding low-value AI work

Do not use the workspace to generate:

- documentation unsupported by repository evidence;
- giant refactors without measurable outcome;
- duplicate skills with overlapping missions;
- architecture diagrams that merely mirror folders;
- speculative optimizations without baseline;
- “best practice” changes that ignore project constraints;
- tests that only assert implementation details;
- notebook content that duplicates source code.

## Executive outcome report

For substantial missions, summarize value using:

```text
Objective:
Baseline:
Changes/decisions:
Evidence:
Measured result:
Risk reduced:
Residual risk/unknowns:
Documentation/knowledge updated:
Recommended next highest-value action:
```

This keeps AEOS aligned with outcomes instead of activity volume.
