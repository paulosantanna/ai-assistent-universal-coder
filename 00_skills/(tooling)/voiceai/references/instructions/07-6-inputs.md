<!-- Package: 00_skills/(tooling)/voiceai; relative command/resource examples resolve from that package or workspace root. -->

## 6. Inputs

Required:

- User objective.
- One of:
  - approved live audio connector session;
  - local drive or mounted drive path that the user supplied for audio/video transcription;
  - approved audio or video file reference;
  - already produced transcript that requires voice-intent processing.
- Activation consent for the current session. If the user gives no explicit retention policy, default to transient raw audio/video processing and retain only redacted transcript/evidence refs required by AEOS.

Optional:

- Repository path or AEOS package scope.
- Target artifact type: skill, MCP, LSP, playbook, guardrail, prompt, report or implementation task.
- Preferred transcription engine or model.
- Domain vocabulary, acronyms, names and expected languages.
- Maximum retention window for raw audio, video-derived audio and transcript artifacts.
- Redaction policy for secrets, personal data and sensitive content.
