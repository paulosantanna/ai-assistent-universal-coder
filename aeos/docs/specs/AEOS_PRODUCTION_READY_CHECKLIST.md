# AEOS Production Ready Checklist

## Required PASS

- [ ] Kernel Runtime enabled.
- [ ] Deny-all permission model active.
- [ ] Policy Engine fail-closed.
- [ ] Tool Router required.
- [ ] MCP registry allowlisted.
- [ ] Critical MCPs disabled by default.
- [ ] Evidence manifest generated.
- [ ] Evidence verify command passes.
- [ ] Judge deterministic gates pass.
- [ ] Approval gateway granular and expiring.
- [ ] No wildcard approval accepted.
- [ ] Secrets redaction eval passes.
- [ ] Package verify blocks path traversal.
- [ ] Package verify blocks secrets.
- [ ] CI gates exist.
- [ ] Test runner allowlist active.
- [ ] Rollback works for patch apply.
- [ ] Observability emits logs/traces/metrics.
- [ ] SLO budgets configured.
- [ ] Incident runbooks exist.
- [ ] Supply-chain checks configured.
- [ ] Release gate blocks if critical failure exists.
