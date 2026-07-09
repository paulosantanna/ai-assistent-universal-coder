# Risk Classifier Skill

**ID:** risk-classifier
**Version:** 1.0.0
**Owner Agent:** security
**Risk Level:** low

## Mission
Classify the risk level of proposed changes — considering scope, impact, reversibility, test coverage, and security implications.

## Scope
- Analyze proposed changes and context
- Classify each change with risk level
- Generate mitigation recommendations for high/critical risks

## Allowed Actions
- `filesystem.read` — read patches, analysis reports
- `generate_evidence` — register risk classifications

## Forbidden Actions
- Modify any file
- Block or approve changes directly (decision is input for Judge)
- Override deterministic Judge rules

## Required Capabilities
- ANALYZE_RISK
- GENERATE_REPORT

## Required Evidence
- Patch/source analysis (SHA-256)
- Risk classification report

## Quality Gates
- Risk levels must be one of: low, medium, high, critical
- High/critical MUST have mitigation strategy
- Classification must cite evidence

## Output Schema
```json
{
  "overall_risk": "medium",
  "risks": [
    {"risk": "API breakage", "level": "high", "mitigation": "Add deprecation warning, keep backward compat for 1 release",
     "evidence": ["src/api/v1/users.py:45"]},
    {"risk": "Security regression", "level": "medium", "mitigation": "Add input validation tests",
     "evidence": ["src/auth/validator.py:12"]}
  ],
  "safe_to_propose": true
}
```

## Blocking Conditions
- High risk without any mitigation
- Risk classification contradicts obvious severity
- Insufficient evidence for classification