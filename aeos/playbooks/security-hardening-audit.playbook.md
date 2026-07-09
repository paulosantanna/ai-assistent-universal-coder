# Playbook: security-hardening-audit

## Objective

Audit AEOS hardening controls before v1.0.

## Steps

1. Generate threat model.
2. Validate deny-all permission model.
3. Validate policy coverage.
4. Validate Tool Router enforcement.
5. Validate MCP critical connectors disabled.
6. Validate package quarantine.
7. Validate redaction and secret blocking.
8. Validate evidence integrity.
9. Generate hardening report.
10. Run Judge.

## Blocking Conditions

- critical MCP enabled by default;
- direct tool bypass;
- raw secrets persisted;
- package extraction without verify;
- approval global wildcard allowed;
- Judge deterministic failure can be bypassed.
