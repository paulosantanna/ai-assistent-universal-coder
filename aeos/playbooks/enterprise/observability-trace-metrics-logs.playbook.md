# Enterprise Playbook: observability-trace-metrics-logs

## Objective

Implement a portable observability package for any requested project, language,
architecture or backend with traces, metrics, logs and automatically generated
dashboards for Grafana, open-source Grafana-compatible stacks or Dynatrace.

## Inputs

- target project path;
- service name;
- language or languages;
- architecture;
- backend: `grafana`, `dynatrace` or `stdout`;
- required SLOs and business KPIs;
- deployment target.

## Required Agents

- Root
- Architect
- DevOps
- Tester
- Security
- Judge

## Required MCPs

- filesystem-readonly
- filesystem-write-sandbox
- test-runner-controlled
- docs-opentelemetry
- docs-grafana
- docs-dynatrace
- docs-observability-dashboards

## Steps

1. Inspect project stack, language boundaries and deployment model.
2. Load official/guided documentation through the observability MCPs.
3. Choose instrumentation strategy per language without overwriting user code.
4. Generate an observability package in sandbox:
   - `otel-collector.yaml`;
   - `grafana-dashboard.json`;
   - `dynatrace-dashboard.json`;
   - `instrumentation-checklist.md`.
5. Map required signals:
   - request rate;
   - error rate;
   - duration and latency percentiles;
   - traces and span volume;
   - structured logs and correlation IDs;
   - SLO and business KPI panels.
6. Validate dashboards against backend rules and no-secret policy.
7. Run available project tests and AEOS contract validators.
8. Emit evidence and Judge result.

## Generation Command

```bash
python aeos/scripts/observability_package.py --target .aeos/tmp/observability/<service> --service-name <service> --language <language> --backend grafana
```

## Blocking Conditions

- target project cannot be inspected;
- backend is unknown;
- language is unknown;
- required signal cannot be mapped;
- generated dashboard contains secrets;
- generated package cannot be validated;
- Judge fails.

## Outputs

- `.aeos/tmp/observability/<service>/otel-collector.yaml`
- `.aeos/tmp/observability/<service>/grafana-dashboard.json`
- `.aeos/tmp/observability/<service>/dynatrace-dashboard.json`
- `.aeos/tmp/observability/<service>/instrumentation-checklist.md`
- evidence report with source documentation references
