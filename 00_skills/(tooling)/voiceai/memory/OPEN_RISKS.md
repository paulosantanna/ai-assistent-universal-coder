# OPEN_RISKS.md

Open risks for `voiceai`:

- Activation is consent for the current session, but runtime recording still depends on an approved audio connector and OS/tool permission.
- No transcription engine is bundled. Speech-to-text execution depends on an approved local or remote engine with known retention behavior.
- Video transcription depends on an approved media extractor before speech-to-text.
- Direct cloud Drive access is blocked unless the drive is mounted locally or exposed by an approved connector.
- Mixed-language detection quality depends on the chosen engine and may require user confirmation for low-confidence segments.
- Voice-derived instructions can be ambiguous; high-impact artifact generation requires handoff review before execution.

