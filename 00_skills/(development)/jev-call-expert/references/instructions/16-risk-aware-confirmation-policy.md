<!-- Package: 00_skills/(development)/jev-call-expert; relative command/resource examples resolve from that package or workspace root. -->

## Risk-Aware Confirmation Policy

| Action Type | Confidence Required | Confirmation Needed |
|-------------|--------------------|---------------------|
| Read-only (show balance, display info) | ≥ 0.5 | None |
| Low-stakes mutation (log event, mild flag) | ≥ 0.7 | Optional |
| Medium-stakes mutation (route change, moderate priority) | ≥ 0.8 | Required |
| High-stakes mutation (financial transfer, critical alert) | ≥ 0.95 | Required + explicit confirmation |
| Critical-stakes (destructive, security-sensitive) | ≥ 0.99 | Human-supervised only |

**Never use Jev confidence as authorization.** Always preserve:
- Permission checks in code
- Authorization rules
- Explicit user confirmation for consequential actions
- The repository's required approval path
