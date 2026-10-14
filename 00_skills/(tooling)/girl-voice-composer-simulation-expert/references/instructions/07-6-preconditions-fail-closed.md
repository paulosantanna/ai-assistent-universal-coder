<!-- Package: 00_skills/(tooling)/girl-voice-composer-simulation-expert; relative command/resource examples resolve from that package or workspace root. -->

## 6. Preconditions (fail closed)

Before producing parameters, verify:

1. **Purpose is generic/fictional.** The output is not intended to impersonate a
   real, identifiable child. If it is, **STOP** with status `BLOCKED`.
2. **Consent gate (conditional).** If any real recordings of minors are used to
   *inform* tuning, a **consent artifact reference** (provider/identifier/path,
   never the content) MUST be present. If real recordings are involved and the
   consent reference is absent, **STOP** with status `BLOCKED`.
   - Consent reference is stored **by pointer only**. Never copy recording
     content, transcripts, personal data, or extracted voiceprints into any
     skill file, evidence, memory, or log.
3. **Language supported.** Target language ∈ {pt-BR, en-US}. Otherwise `BLOCKED`.
4. **Age band.** Target perceived age ∈ [6, 8]. Otherwise `BLOCKED`.
5. **Engine declared.** A target engine and its parameter surface are provided,
   OR the user explicitly requests an engine-agnostic reference spec.

See `templates/consent_gate.md` for the required consent-reference shape.

---
