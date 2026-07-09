# AEOS v1.0 Release Guide

## Release checklist

- Run `v1-readiness-audit`.
- Run `security-hardening-audit`.
- Run `pack-marketplace-audit`.
- Run `tool-router-audit`.
- Run `mcp-health-check`.
- Run evidence verify for all sample executions.
- Run package verify for all exported packs.
- Confirm no auto-merge.
- Confirm no auto-deploy.
- Confirm secrets are redacted.
- Confirm critical MCPs disabled by default.
