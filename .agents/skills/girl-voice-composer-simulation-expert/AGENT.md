# AGENT.md — girl-voice-composer-simulation-expert

This skill is a capability of `codenavi-agent`. It creates no new agent
identity.

## Operating contract

- State language, age, style, engine, and consent status before emitting params.
- Refuse impersonation of identifiable minors; proceed only with generic,
  fictional direction.
- Fail closed when the consent gate applies and no reference is present.
- Never process audio; never claim a voice was "learned" from a recording.
- Persist only generic tuning lessons; never personal data or recording content.

## Verification

- `python scripts/validate_profile.py <profile.json>` must exit `0`.
- `python tests/test_validate_profile.py` must exit `0`.
