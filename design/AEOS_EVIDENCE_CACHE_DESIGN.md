# AEOS Evidence Cache Design

## Status: Design Document (Not Implemented)

## Objective
Design a cache system for AEOS evidence to avoid redundant computations across executions.

## Cache Key Requirements

The cache key MUST be derived from a combination of:

1. **Config hash** — SHA-256 of `aeos/config/aeos.config.yaml`
2. **Playbook version** — version field from playbook definition
3. **Skill version** — version field from each skill used
4. **File content hashes** — SHA-256 of all input files (target source files)
5. **Target path** — normalized absolute path of execution target

### Cache Key Structure

```python
cache_key = sha256(
    config_hash +
    playbook_version +
    skill_versions (sorted) +
    input_file_hashes (sorted) +
    normalized_target_path
)
```

## Invalidation Rules

1. **Automatic invalidation** when ANY input changes:
   - Config file modified → cache invalidated
   - Playbook version changed → cache invalidated
   - Skill version changed → cache invalidated
   - Any input file content hash changed → cache invalidated
   - Target path changed → cache invalidated

2. **Manual invalidation**:
   - CLI flag: `aeos run --no-cache <playbook>`
   - Clear cache: `aeos cache clear`

## Security Constraints

1. **ABSOLUTELY PROHIBITED**: Using cache for secrets/security scans without revalidation.
   - `security-secrets-audit` MUST never use cached results
   - Any playbook with `risk_level: high` or `risk_level: critical` must revalidate
   - Cache entries for security playbooks must be ignored

2. **Evidence integrity**: Cached evidence must still pass SHA-256 verification.

## Storage

- Cache directory: `.aeos/cache/`
- Each entry: `.aeos/cache/{cache_key_prefix}/`
- Cache manifest: `.aeos/cache/cache-manifest.json`
- Max cache age: 7 days (configurable)
- Max cache size: 500MB (configurable)

## Cache Entry Format

```json
{
  "cache_key": "sha256hex...",
  "created_at": "2026-07-08T20:00:00Z",
  "playbook_id": "documentation-generation",
  "config_hash": "sha256hex...",
  "playbook_version": "1.0.0",
  "skill_versions": {"documentation": "1.0.0"},
  "input_file_count": 218,
  "target_path": "/workspace/project",
  "expires_at": "2026-07-15T20:00:00Z",
  "artifact_count": 5,
  "total_size_bytes": 10240,
  "security_revalidation_required": false
}
```

## Not Implemented in v0.2.1

This design is a roadmap reference only. No cache functionality is implemented.

## Future Implementation Notes

- Implement in `aeos_workbench/execution/cache_manager.py`
- Integrate with `ExecutionOrchestrator` as optional step before `_execute_playbook`
- Add CLI cache commands: `aeos cache clear`, `aeos cache status`
- Add `--no-cache` flag to `aeos run`