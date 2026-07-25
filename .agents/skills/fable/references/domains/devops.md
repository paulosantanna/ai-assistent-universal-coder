# Domain adapter: devops and infrastructure

Applies when the deliverable changes how a system runs: infrastructure-as-code (Terraform, CloudFormation, Kubernetes manifests, Ansible), CI/CD pipeline configs, deployment or rollback scripts, monitoring and alerting rules, runbooks, and incident postmortems.

## Minimum evidence set (binding, before any change is applied)

1. **The current live state**: the actual running config, deployed version, or infra state (a plan/diff output, live `kubectl get`, dashboard reading).
2. **The governing runbook or policy**: change-management doc, SLO, or on-call runbook.
3. **One live platform reference**: current provider docs or CLI behavior, fetched now.

## Evidence and primary sources

The system's actual observed state, plan output, re-read config, metric, log line is primary source. Non-evidence: green pipeline or apply command exiting 0 is not evidence of system health; post-change health check or metric is.

## Authority order

Explicit user instruction > runbook policy > platform behavior > IaC file intent > personal judgment.

## Verification by observation

- Change confirmed applied to target system (plan/diff, live config read, metric/log line).
- Blast radius named before irreversible action; rollback path reviewed.
- Health checked post-change: latency, error rates, alerts.
- Outward/irreversible steps follow authorization gate (`AUTH:`).

## Fraud table (for fable-judge)

| Fraud | Symptom |
|---|---|
| Big-bang deploy | change pushed to all hosts without canary/rollout |
| Silenced alerting | threshold widened or check disabled to hide root cause |
| Untested rollback | deploy with no rollback path or unvalidated rollback |
| Config drift denial | claiming system matches IaC without checking live state |
| Secret in clear | credentials committed to IaC or configs |
| Unauthorized prod touch | apply/deploy without quoted user authorization |

## Done, by example

"The staging deploy is done" means: plan reviewed before apply, change confirmed live, health checked post-change, rollback path stated, prod steps authorized.
