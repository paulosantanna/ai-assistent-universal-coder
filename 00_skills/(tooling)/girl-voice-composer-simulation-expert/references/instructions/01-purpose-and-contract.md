<!-- Package: 00_skills/(tooling)/girl-voice-composer-simulation-expert; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# Girl Voice Composer — Simulation Expert

> Canonical AEOS Level-3 governed skill for **parametric direction** of a
> generic, fictional female child voice (perceived age band 6–8) in **pt-BR**
> and **en-US**.
>
> This skill produces **acoustic direction parameters** for an external
> TTS / voice-design engine. It does **not** contain, embed, extract, or
> reconstruct the voice of any real, identifiable child.

```yaml
skill:
  name: Girl Voice Composer — Simulation Expert
  slug: girl-voice-composer-simulation-expert
  version: 1.0.0
  description: >-
    Parametric direction of a generic fictional female child voice (age 6-8)
    for an external TTS engine, in pt-BR and en-US.
  category: GENERATION
  architecture_level: 3
  risk_level: HIGH
  activation:
    - request to configure, direct or generate a female child voice profile
    - request for child voice acoustic parameters (pitch, formants, prosody, EQ)
    - request to tune a TTS engine to a young-girl timbre in pt-BR or en-US
  exclusions:
    - cloning or replicating a specific real person's voice
    - deepfake or impersonation of an identifiable minor
    - biometric voiceprint extraction from source recordings
    - adult voice synthesis
    - unrelated audio DSP tasks
  inputs:
    - target language (pt-BR | en-US)
    - target perceived age within 6-8
    - target TTS/voice-design engine identifier and its parameter surface
    - text to be voiced
    - consent artifact reference (identifier/path only) when real recordings inform tuning
  outputs:
    - validated voice parameter set (JSON matching schema)
    - per-language prosody and pronunciation direction notes
    - engine-mapping notes and known limitations
  tools:
    - filesystem (skill directory only)
    - Python (deterministic validation)
  memory: true
  human_approval: conditional
  maintainer: Paulo
```

---
