# AEOS Policy Engine

## Purpose

Policy Engine validates whether an action is globally acceptable, even if permissions would otherwise allow it.

## Difference from Permission Engine

Permission Engine asks:

```text
Can this actor perform this capability?
```

Policy Engine asks:

```text
Is this action allowed under AEOS global law and project policy?
```

## Global Policies

- Block destructive actions without approval.
- Block writes outside sandbox unless approved.
- Block secrets in outputs.
- Block direct tool access.
- Block commit/push/merge without approval.
- Block protected branch mutation.
- Block shell commands outside allowlist.
- Block ZIP packages without manifest and checksums.
- Block package extraction without verification.

## Severity

```yaml
severity:
  info
  warning
  high
  critical
```

Critical policy failure forces `BLOCKED`.
