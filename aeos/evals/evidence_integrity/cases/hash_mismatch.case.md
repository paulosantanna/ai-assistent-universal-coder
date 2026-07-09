---
description: "Validate that real hash mismatch is detected (mismatch → FAIL)"
severity: high
expected: FAIL
blocking: true
inputs:
  type: evidence_integrity
  hash: "abc123"
  expected_hash: "different_hash"
---
# Eval Case: hash_mismatch

## Suite

evidence_integrity

## Objective

Validate AEOS detection of real hash mismatch after file tampering.

Creates a scenario where two hashes intentionally differ to verify
that the integrity check correctly detects a mismatch and reports FAIL.
This is NOT a lifecycle false positive — it tests detection of actual
data corruption after manifest finalization.

## Expected

- hash mismatch is detected;
- case reports FAIL when hash != expected_hash;
- lifecycle temporary files are NOT confused with real corruption.

## PASS Criteria

- FAIL when hash differs from expected_hash (mismatch detected);
- PASS only when hashes match (integrity verified);
- real corruption is blocked;
- lifecycle state is not mistaken for tampering.
