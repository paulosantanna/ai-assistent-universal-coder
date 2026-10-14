# voiceai

`voiceai` is a governed AEOS skill for current-session consent-based speech intake, direct authorized drive/media access, video-audio transcription, literal multilingual transcription and voice-intent routing.

It preserves the exact spoken transcript, identifies mixed-language segments, separates jokes or out-of-scope speech from actionable work, and turns relevant spoken intent into AEOS handoff drafts for skills, MCPs, LSPs, playbooks, guardrails and related artifacts.

## Activation

Use this skill when a user asks AEOS to process voice/audio input, record the current session, transcribe audio from videos, read user-authorized local or mounted drive media paths, handle mixed-language spoken instructions or create governed AEOS artifacts from speech.

## Key Rules

- Activating `voiceai` is explicit consent for current-session recording or transcription within the declared scope.
- Direct local-drive or mounted-drive access is limited to user-supplied audio/video paths.
- Cloud Drive access requires a mounted drive or approved connector authorization.
- Literal transcription is produced before any summary or normalization.
- Language identification is segment-level and must support mixed-language utterances.
- Jokes and out-of-scope speech stay in the transcript but do not become task scope unless explicitly reclassified by the user.
- Voice-derived artifact creation must route through AEOS handoffs and generators.

## Validation

```bash
py -3 scripts/validate.py .
```

