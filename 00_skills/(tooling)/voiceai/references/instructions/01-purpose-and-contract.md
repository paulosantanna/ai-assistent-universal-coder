<!-- Package: 00_skills/(tooling)/voiceai; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# voiceai

```yaml
skill:
  name: voiceai
  slug: voiceai
  version: 1.0.0
  description: Governed AEOS voice interface where explicit activation grants current-session consent for direct authorized audio capture, direct authorized drive or mounted-path media access, video-audio transcription, literal multilingual transcription, mixed-language segmentation, relevance classification, and conversion of actionable spoken intent into AEOS artifact handoffs.
  category: AI_ML
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests AEOS voice capture, direct audio recording, audio or video transcription, speech-to-text, multilingual voice intent routing, or voice-driven creation of skills, MCPs, LSPs, playbooks, guardrails or related AEOS artifacts
  exclusions:
    - unrelated requests
    - covert recording
    - biometric identification
    - speaker surveillance
    - transcription outside the activated current session or without an authorized audio, video or mounted-drive source
  inputs:
    - user objective
    - authorized audio stream, audio file, video file, local drive path or mounted drive path reference
    - optional repository scope
    - optional target artifact type
    - optional privacy, retention and media-source constraints
  outputs:
    - literal transcript
    - language segments
    - relevance classification
    - actionable intent brief
    - AEOS handoff draft
    - evidence and risk report
  tools:
    - approved audio input connector
    - approved media file reader
    - approved video audio extractor
    - approved speech-to-text engine
    - AEOS Tool Router
    - AEOS Skill Factory
  memory: true
  human_approval: true
  maintainer: AEOS
```
