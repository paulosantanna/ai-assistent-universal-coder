# AEOS Rollback Encryption Design

## Status: Design Document (Not Implemented)

## Objective
Design encryption for `rollback-plan.json` to protect sensitive rollback metadata.

## Rationale

In v0.2.1, `rollback-plan.json` is stored in plaintext. This design documents how to encrypt it in a future version while maintaining usability for automated rollback.

## Encryption Requirements

1. **Algorithm**: AES-256-GCM (authenticated encryption) via cryptography library
2. **Key management**: Key derived from execution passphrase or workspace key
3. **Integrity**: GCM provides authenticated encryption (encrypt-then-MAC)
4. **Metadata**: Only encrypt the `operations` array; keep `execution_id`, `generated_at`, `strategy`, `summary` in plaintext for indexing

## Key Sources (Priority Order)

1. **Execution-specific key**: Generated at execution start, stored in `.aeos/keys/{execution_id}.key.enc`
2. **Workspace key**: Stored in `.aeos/.rollback-key` (encrypted with a configurable passphrase)
3. **Environment variable**: `AEOS_ROLLBACK_KEY`

## Encrypted Structure

```json
{
  "execution_id": "ex-20260708T200909-eb3b99",
  "generated_at": "2026-07-08T20:09:09.367450+00:00",
  "strategy": "sandbox_cleanup",
  "encryption": {
    "algorithm": "AES-256-GCM",
    "key_source": "execution-key",
    "nonce": "base64...",
    "tag": "base64..."
  },
  "operations_encrypted": "base64...",
  "summary": {
    "total_operations": 5,
    "delete_operations": 5
  }
}
```

## Non-Encrypted Metadata

The following fields remain in plaintext:
- `execution_id`
- `generated_at`
- `strategy`
- `summary.total_operations`
- `summary.delete_operations`
- `encryption` metadata (algorithm, nonce, tag)

## Rollback Constraints

1. **Automated rollback**: Only works if key is available at rollback time
2. **Manual rollback**: Human can always manually delete `.aeos/sandbox/{id}/` without the key
3. **Key loss**: If key is lost, manual rollback instructions are printed

## Key Rotation

- Each execution generates a new key
- Old keys can be purged after rollback TTL (default: 30 days)
- Key directory: `.aeos/keys/`

## Not Implemented in v0.2.1

This design is a roadmap reference only. No rollback encryption is implemented.

## Future Implementation Notes

- Implement in `aeos_workbench/execution/rollback_encryption.py`
- Integrate with `RollbackManager` during `save()` and `RollbackManager.load()`
- Add `--encrypt-rollback` flag to `aeos run`
- Add CLI: `aeos rollback decrypt --execution-id <id> --key <key-path>`