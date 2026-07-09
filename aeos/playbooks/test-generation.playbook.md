# Test Generation Playbook

**ID:** test-generation
**Version:** 1.0.0
**Risk Level:** low
**Required Agents:** root, tester, coder, judge
**Required Skills:** test-gap-analyzer, test-writer, code-analyzer, risk-classifier
**Required LCPs:** global-rules
**Allowed MCPs:** filesystem-readonly, filesystem-write-sandbox

## Flow

### Step 1: Detect Test Framework
- Scan target path for test framework indicators
- Check: pytest, unittest, jest, mocha, vitest, junit, pytest-cov
- Return detected framework with confidence

### Step 2: Detect Existing Test Patterns
- Find existing test files in the project
- Analyze naming conventions, directory structure, fixtures, helpers
- Document patterns found

### Step 3: Map Test Gaps
- Compare source files to test files
- Identify untested modules, functions, and edge cases
- Prioritize gaps by risk (security, core logic, error handling)

### Step 4: Generate Proposed Tests in Sandbox ONLY
- Create: .aeos/sandbox/{execution_id}/generated-tests/
- Generate test files following detected patterns
- Each test file MUST include header citing source evidence:
  ```
  # Source: <relative path to real source file>
  # Evidence: SHA-256 of source file
  ```
- Generate test-index.md listing all generated tests

### Step 5: Generate Risk Report
- Write: .aeos/sandbox/{execution_id}/test-risk-report.md
- Include: coverage gaps, untested edge cases, test quality assessment
- Label each entry as Fact, Assumption, Risk, or Recommendation

### Step 6: Generate Rollback Plan
- Write: .aeos/sandbox/{execution_id}/rollback-plan.md
- Rollback = delete all files in .aeos/sandbox/{execution_id}/

### Step 7: Evidence Registration
- Register all generated artifacts in evidence-manifest.json
- Compute SHA-256 for every artifact
- Append to hash-chain.jsonl

## Outputs

| Artifact | Path | Required |
|----------|------|----------|
| Generated tests | `.aeos/sandbox/{execution_id}/generated-tests/` | Yes |
| Test index | `.aeos/sandbox/{execution_id}/generated-tests/test-index.md` | Yes |
| Test risk report | `.aeos/sandbox/{execution_id}/test-risk-report.md` | Yes |
| Rollback plan | `.aeos/sandbox/{execution_id}/rollback-plan.md` | Yes |
| Evidence manifest | `.aeos/evidence/{execution_id}/evidence-manifest.json` | Yes |
| Hash chain | `.aeos/evidence/{execution_id}/hash-chain.jsonl` | Yes |

## Prohibitions
- Do NOT write test files to src/test/ or any real test directory
- Do NOT modify existing test files
- Do NOT run real test suite (analysis only)
- Do NOT commit generated tests

## Blocking Conditions
- Generated test does not cite source file
- Test file written outside .aeos/sandbox/
- No test framework detected (warning, not block)