# NEGATIVE_KNOWLEDGE.md

Known failures and unsafe shortcuts for `voiceai`:

- Treating a summary as the transcript destroys evidence. Preserve the literal transcript first.
- Forcing one language across a mixed-language utterance loses intent and terminology.
- Converting jokes, small talk or out-of-scope speech into task scope creates false requirements.
- Capturing live audio without explicit consent violates the AEOS approval boundary.
- Sending audio to a remote transcription service without checking privacy constraints can leak sensitive data.
- Treating speaker identity, emotion or health as inferable from voice is outside this skill's authority.
- Mutating active registries or creating production artifacts directly from a voice command bypasses AEOS handoff governance.
