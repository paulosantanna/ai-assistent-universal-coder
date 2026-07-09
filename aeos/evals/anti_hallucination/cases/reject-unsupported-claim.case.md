---
description: Reject claim without supporting evidence
severity: critical
expected: PASS
blocking: true
inputs:
  type: anti_hallucination
  claims:
    - claim: "Repository has 1000 stars"
      evidence_refs: []
    - claim: "Code coverage is 95%"
      evidence_refs: ["coverage-report.json"]
  expected_no_unsupported: false
---
