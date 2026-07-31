# POSITIVE_KNOWLEDGE.md

Validated operating patterns for `voiceai`:

- Preserve a literal transcript before summarization, normalization or artifact generation.
- Use segment-level language tags so code-switched phrases can retain each language.
- Keep an out-of-scope ledger for jokes, side remarks and unrelated speech.
- Build actionable intent only from cited transcript segments.
- Route voice-derived artifact creation through the relevant AEOS generator or handoff.
- Report uncertainty when audio quality, language detection or intent classification is weak.
