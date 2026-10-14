# Domain adapter: AEOS Enterprise Skills

Applies when any of the 160+ AEOS skills (e.g. `aeos-code-analyzer`, `aeos-security-audit`, `aeos-architecture-mapper`, `aeos-test-writer`, `aeos-ci-quality-gate-engineer`, `aeos-v1-readiness-auditor`, `aeos-patch-planner`, etc.) is executed.

The Fable Method loop provides supreme governance over AEOS skill executions: it forces evidence gathering before action, Intent Gate before behavior changes, Recall Gate before recalling parameters/signatures, observed verification of target and system health, and an adversarial Judge pass before returning output.

## AEOS Skill to Fable Domain Mapping

| AEOS Skill Category | AEOS Skills Included | Fable Domain Adapter | Minimum Evidence Set |
|---|---|---|---|
| **Code & Architecture** | `aeos-code-analyzer`, `aeos-architecture-mapper`, `aeos-diff-reviewer`, `aeos-patch-planner`, `aeos-legacy-risk-mapper` | **Coding Domain** | Target source files, AST/dependency tree, AST import spec |
| **Testing & Quality** | `aeos-test-writer`, `aeos-test-generation`, `aeos-test-gap-analyzer`, `aeos-ci-quality-gate-engineer` | **Coding / DevOps Domain** | Existing test suite, build config, live test execution output |
| **Infrastructure & DevOps** | `aeos-docker-devcontainer-engineer`, `aeos-observability-architect`, `aeos-production-deployment-planner` | **DevOps & Infra Domain** | Live infra state (`kubectl`, plan/diff), governing runbook, provider docs |
| **Security & Compliance** | `aeos-security-audit`, `aeos-enterprise-security-auditor`, `aeos-secret-redaction-specialist`, `aeos-compliance-evidence-exporter` | **Legal & Compliance Domain** | Statutory/regulatory spec, SAST scan output, gitleaks log |
| **AI, RAG & Performance** | `aeos-python-ai-productionizer`, `aeos-performance-profiler`, `aeos-cost-token-optimizer`, `aeos-slo-risk-analyzer` | **Data & Performance Domain** | Benchmark metrics, trace log, conformal prediction threshold |
| **Governance & Release** | `aeos-release-readiness-judge`, `aeos-v1-readiness-auditor`, `aeos-delegation-auditor`, `aeos-approval-governance-auditor` | **fable-judge Domain** | Independent diff, clean build output, evidence manifest |

---

## Universal Fable Loop Execution Protocol for AEOS Skills

### Step 0 & 1 - Classify & Define Done
- Classify the AEOS skill invocation shape (Task, Assessment, Plan-first).
- Define concrete done criterion and verification method before invoking the skill.

### Step 2 - Gather Evidence
- Open primary sources (file:line, build config, live CLI output) before executing skill logic.
- Never assume file contents or skill inputs from memory.

### Step 3 - Decide & Commit
- Formulate single recommendation.
- Check Authorization Gate (`AUTH: user said "..."`) before any outward or irreversible action.

### Step 4 - Act Surgically
- Write `INTENT:` line before any code, configuration, or state modification.
- Execute smallest correct change.

### Step 5 - Observe Verification & Twin Check
- Execute target check AND verify surrounding system health.
- Execute `TWINS:` search sweep whenever a defect is fixed.

### Step 6 - Outcome-First Report & Fable Judge Pass
- Pass output through `aeos-fable-judge` adversarial review.
- Return plain-language outcome first, with zero step headers, accompanied by INTENT, AUTH, TWINS, and PENDING lines when applicable.
