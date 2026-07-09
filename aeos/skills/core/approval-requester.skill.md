# Approval Requester Skill

**ID:** approval-requester
**Version:** 1.0.0
**Owner Agent:** root
**Risk Level:** low

## Mission
Determine what approvals are needed for a proposed change, create approval requests, and track approval status.

## Scope
- Assess change scope and risk
- Determine required approvals (action + scope)
- Create approval requests in .aeos/approvals/
- Check approval status

## Allowed Actions
- `filesystem.read` — read patch and analysis files
- `filesystem.write_aeos` — write to .aeos/approvals/
- `generate_evidence` — register approval requests

## Forbidden Actions
- Approve or deny on behalf of human
- Create global unrestricted approvals (scope="**")
- Auto-approve without human review

## Required Capabilities
- READ_REPOSITORY
- MANAGE_APPROVALS
- GENERATE_REPORT

## Required Evidence
- Approval requests created (paths with SHA-256)
- Approval status report

## Quality Gates
- No approval with unrestricted scope (**)
- Each approval must have: execution_id, action, scope, expiration
- Approvals beyond 90 days must be flagged

## Output Schema
```json
{
  "approval_id": "ap-a1b2c3d4",
  "execution_id": "ex-20260101T120000-abc123",
  "action": "patch.propose",
  "scope": ".aeos/patches/**",
  "status": "pending",
  "expiration": "2026-02-01T00:00:00+00:00"
}
```

## Blocking Conditions
- Attempt to create approval with scope "**" or "all"
- Approval executed without human decision
- Approval for an action not in granular list