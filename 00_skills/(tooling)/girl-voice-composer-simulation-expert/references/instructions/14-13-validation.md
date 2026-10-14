<!-- Package: 00_skills/(tooling)/girl-voice-composer-simulation-expert; relative command/resource examples resolve from that package or workspace root. -->

## 13. Validation

The package passes only when:

- `voice_params.json` validates against the schema (exit code `0`);
- language ∈ {pt-BR, en-US} and age ∈ [6,8];
- no forbidden placeholder remains;
- engine mapping resolves to declared controls (or `agnostic`);
- consent gate satisfied when real recordings are involved.

Run: `python scripts/validate_profile.py <path-to-voice_params.json>`

---
