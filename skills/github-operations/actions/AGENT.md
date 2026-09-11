# Local AGENT contract — github-operations/actions

This subtree inherits root `AGENT.md` and `skills/github-operations/AGENT.md`. It does not define an agent or subagent identity.

## Action-recovery specialization

- Model each workflow as `WorkflowGuardianLens` and each job/matrix child as `JobGuardianWorkUnit` under `codenavi-agent`.
- Establish current head SHA and required-check policy before monitoring.
- Redact logs before any reasoning or persistence.
- Fingerprint/group equivalent failures before assigning a specialist lens.
- Reproduce deterministic failures locally when feasible.
- Apply the smallest root-cause fix; never mask the gate.
- After corrective push, invalidate old-SHA CI evidence and rediscover all relevant runs/checks.
- Continue only while progress and budgets remain.
- Merge readiness requires all required latest-SHA checks green plus governance gates.

## Prohibited

No repository deletion, force-push, branch-protection bypass, secret-value extraction, PAT scope escalation, hidden CI weakening or creation of new agent/subagent identities.
