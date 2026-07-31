# Observability Root Cause Integrator

Autonomous Staff observability skill for Cross-tool RCA analysis.

This package was generated with the AEOS Skill Factory and customized for isolated deep analysis. It is intended to be used directly or through the `analayze-metricas` playbook.

## Isolation

The agent does not communicate with other tool agents. It emits evidence and a handoff artifact for the root-cause integrator.

## Main Outputs

- `tool_analysis_report.json`
- `evidence-index.md`
- `knowledge-candidates.md`
- `handoff-to-root-cause-integrator.json`
