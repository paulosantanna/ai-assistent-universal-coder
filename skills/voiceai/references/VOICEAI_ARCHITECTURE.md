# VOICEAI_ARCHITECTURE.md

`voiceai` uses a staged voice-intent pipeline:

1. Activation-as-current-session-consent and retention gate.
2. Approved audio/video source intake from microphone, file, local drive path or mounted drive path.
3. Video audio extraction when media input is video.
4. Literal speech-to-text transcription.
5. Segment-level language tagging.
6. Relevance classification.
7. Actionable intent extraction from cited segments.
8. AEOS handoff drafting for the target artifact route.
9. Validation, honest evaluation and evidence reporting.

The skill package does not bundle a microphone driver, media extractor or transcription model. Those are runtime dependencies that must be approved and evidenced by AEOS before recording, video-audio extraction or transcription is claimed.

