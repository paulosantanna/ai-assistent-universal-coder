# Consent gate (conditional)

This gate applies ONLY when real recordings of minors are used to *inform*
tuning. If the profile is fully generic and no real recordings are used, set
`consent_ref` to `null` and keep `generic_and_fictional: true`.

## Hard rules
- Store a **reference/identifier only** (provider + opaque id, or a path to an
  externally managed consent record). NEVER store:
  - the recording content,
  - transcripts,
  - the child's name or any personal data,
  - any extracted voiceprint.
- If real recordings are involved and no consent reference is present -> STOP
  with status `BLOCKED`.
- This skill still never clones or reconstructs a specific child's identity.
  Consent does not authorize impersonation of an identifiable minor.

## Required reference shape (example, pointer only)
```json
{
  "consent_ref": "consent-store://guardian-consent/2026-09-16/REC-000123"
}
```

The value above is an opaque pointer. Its resolution and storage of the actual
signed consent live outside this repository and outside these artifacts.
