# Refactoring Proposal Playbook

**ID:** refactoring-proposal
**Version:** 1.0.0
**Risk Level:** high
**Required Agents:** root, architect, coder, tester, security, judge
**Required Skills:** code-analyzer, patch-planner, diff-reviewer, test-gap-analyzer, risk-classifier, rollback-planner, approval-requester, architecture-mapper
**Required LCPs:** global-rules, security-governance
**Allowed MCPs:** filesystem-readonly, filesystem-write-sandbox, git-readonly

## Flow

### Step 1: Validate Justification
- Verify the `--scope` parameter contains a clear objective
- Block refactoring if no objective justification is provided
- Justification must answer: WHY is this refactoring necessary?

### Step 2: Map Current Architecture
- Use architecture-mapper skill
- Identify current module structure, dependencies, patterns
- Document current behavior as evidence

### Step 3: Analyze Affected Files
- Trace all files that would be affected by the refactoring
- Include: source files, test files, config files, type definitions
- Generate affected-files.json

### Step 4: Classify Risk
- Assess: API breakage, behavior change, performance impact, test breakage
- Risk levels: low, medium, high, critical
- High/critical risk MUST have mitigation strategy

### Step 5: Assess Architectural Impact
- Document: coupling changes, interface changes, dependency direction changes
- Assess module boundary changes
- Document: before/after architecture

### Step 6: Generate Proposed Patch
- Create: .aeos/patches/{execution_id}/proposed.patch
- Only diff — do NOT apply
- Generate: patch-summary.md, affected-files.json

### Step 7: Generate Required Tests
- Create: .aeos/sandbox/{execution_id}/generated-tests/
- Tests must verify behavior preservation (before vs after)

### Step 8: Generate Rollback Plan
- Write: rollback-plan.md in patches dir
- Every changed file must have an undo operation
- Include verification steps

### Step 9: Execute Judge v3
- Load full execution context into JudgeV3
- Check all deterministic blocking rules
- Special checks for refactoring:
  - Must have objective justification
  - Must have current architecture evidence
  - Must have behavioral preservation tests

## Outputs

| Artifact | Path | Required |
|----------|------|----------|
| Proposed patch | `.aeos/patches/{execution_id}/proposed.patch` | Yes |
| Affected files | `.aeos/patches/{execution_id}/affected-files.json` | Yes |
| Patch summary | `.aeos/patches/{execution_id}/patch-summary.md` | Yes |
| Rollback plan | `.aeos/patches/{execution_id}/rollback-plan.md` | Yes |
| Risk analysis | `.aeos/patches/{execution_id}/risk-analysis.md` | Yes |
| Architecture evidence | `.aeos/patches/{execution_id}/architecture-evidence.md` | Yes |
| Generated tests | `.aeos/sandbox/{execution_id}/generated-tests/` | Yes |
| Refactoring report | `.aeos/reports/{execution_id}/refactoring-proposal.md` | Yes |
| Judge report | `.aeos/reports/{execution_id}/judge-report.md` | Yes |
| Evidence manifest | `.aeos/evidence/{execution_id}/evidence-manifest.json` | Yes |
| Hash chain | `.aeos/evidence/{execution_id}/hash-chain.jsonl` | Yes |

## Prohibitions
- Do NOT apply refactoring to real files
- Do NOT change public APIs without explicit justification
- Do NOT introduce breaking changes without rollback plan
- Do NOT refactor without evidence of current behavior

## Blocking Conditions
- No objective justification (WHY is missing)
- No current architecture evidence
- No behavioral preservation tests
- No rollback plan
- High risk without mitigation