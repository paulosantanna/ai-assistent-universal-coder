# Playbook: pack-marketplace-audit

## Objective

Validate local AEOS pack marketplace safety.

## Steps

1. Inspect quarantine/staging/active pack dirs.
2. Verify manifests.
3. Verify checksums.
4. Scan for secrets.
5. Validate skill/playbook/LCP/MCP contracts.
6. Validate capability compatibility.
7. Generate marketplace audit report.
8. Run Judge.

## Blocking Conditions

- active pack without verification;
- pack imported directly to active;
- missing manifest;
- checksum mismatch;
- forbidden capability;
- secret detected.
