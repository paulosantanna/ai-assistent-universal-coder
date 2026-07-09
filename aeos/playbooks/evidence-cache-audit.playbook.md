# Playbook: evidence-cache-audit

## Objective

Audit Evidence Cache safety and invalidation behavior.

## Steps

1. Load evidence cache config.
2. Validate allowed and forbidden cache types.
3. Validate cache key strength.
4. Validate file content hashes.
5. Validate policy/permission/config hash inclusion.
6. Detect stale cache.
7. Generate cache audit report.
8. Run Judge.

## Blocking Conditions

- weak cache key;
- secret cached;
- approval reused as cache permission;
- missing invalidation rule;
- stale cache accepted.
