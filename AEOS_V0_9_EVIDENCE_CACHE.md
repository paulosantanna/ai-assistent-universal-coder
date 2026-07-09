# AEOS v0.9 — Evidence Cache

## Purpose

Reduce repeated work without trusting stale evidence.

## Core Rule

Evidence cache is never used unless all inputs match.

## Cache Key

```text
cache_key = sha256(
  aeos_version
  + config_hash
  + policy_hash
  + permission_hash
  + playbook_id
  + playbook_version
  + skill_versions
  + lcp_versions
  + mcp_versions
  + target_path
  + file_content_hashes
  + command_inputs
)
```

## Cache Types

```text
stack_detection_cache
dependency_analysis_cache
architecture_map_cache
test_detection_cache
security_scan_cache_metadata_only
```

## Forbidden Cache

Do not cache:

- raw secrets;
- raw logs with credentials;
- browser sessions;
- tokens;
- cookies;
- secret scan values;
- approval decisions as reusable permissions;
- production mutation results.

## Invalidation

Invalidate when:

- file hash changes;
- config changes;
- policy changes;
- permission changes;
- skill/playbook/LCP changes;
- AEOS version changes;
- target path changes;
- security policy changes.

## Judge Rules

Judge must report whether cache was used and why it was valid.
