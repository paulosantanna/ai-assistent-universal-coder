# analayze-metricas

AEOS playbook for deep observability analysis across Dynatrace, Grafana, Kubernetes, OpenShift and Splunk.

The spelling `analayze-metricas` is preserved because it is the requested playbook name. The playbook also declares aliases for corrected spellings.

## Model

Specialist agents run independently and do not communicate with each other. Each specialist emits evidence and a handoff artifact. The `observability-root-cause-integrator` consumes those artifacts and repository code context to produce a Staff-level remediation plan.

## Output

- Tool-specific evidence reports.
- Cross-tool timeline.
- Contradiction matrix.
- Root-cause candidates.
- Code correlation.
- Simple low-impact remediation plan.
- Verification and rollback plan.
