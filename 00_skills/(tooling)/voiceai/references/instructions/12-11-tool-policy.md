<!-- Package: 00_skills/(tooling)/voiceai; relative command/resource examples resolve from that package or workspace root. -->

## 11. Tool Policy

- Activation of `voiceai` is explicit user authorization for current-session live microphone capture when the user requests recording, subject to OS/tool permissions and approved connector availability.
- Direct local-drive or mounted-drive access is limited to user-supplied paths and declared media scope. Cloud Drive access requires the drive to be mounted locally or exposed through an approved connector with its own authorization.
- Video transcription requires an approved media reader/extractor and then an approved speech-to-text engine with declared retention behavior.
- Speech-to-text requires an approved local or remote transcription engine with declared retention behavior.
- Remote transcription is blocked when privacy constraints prohibit sending audio outside the local environment.
- Artifact creation must use the relevant AEOS generator or handoff path; voiceai must not bypass skill, MCP, LSP, playbook or guardrail governance.
- Direct registry mutation, production deployment, destructive filesystem operations and credential handling require the normal AEOS approval boundary.
