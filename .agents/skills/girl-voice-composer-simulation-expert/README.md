# girl-voice-composer-simulation-expert

AEOS Level-3 governed skill that **directs a TTS / voice-design engine** to
synthesize a **generic, fictional female child voice** (perceived age 6–8) in
**pt-BR** and **en-US**.

It emits bounded acoustic parameters (pitch, formants, prosody, syllable
rhythm, EQ, dynamics), per-language direction notes, an engine mapping, and an
explicit limitations statement.

## What this skill does NOT do

- It does **not** process audio or "learn" a voice from any recording/video.
- It does **not** clone, mimic, or reconstruct the voice of any **real,
  identifiable child** (that is an explicit non-activation / `BLOCKED` case).
- It does **not** promise perfect, glitch-free, human-indistinguishable output.
  Final quality depends on the downstream engine and must be verified by
  listening.

## Structure

```text
girl-voice-composer-simulation-expert/
├── SKILL.md
├── README.md
├── AGENT.md
├── scripts/
│   └── validate_profile.py
├── schemas/
│   └── voice_profile.schema.json
├── templates/
│   ├── parameter_defaults.md
│   ├── prosody_pt-BR.md
│   ├── prosody_en-US.md
│   ├── engine_coqui_xtts.md
│   ├── engine_piper.md
│   ├── post_processing.md
│   ├── consent_gate.md
│   └── example_voice_params.json
├── tests/
│   └── test_validate_profile.py
├── knowledge/
│   ├── KNOWLEDGE.md
│   ├── POSITIVE_KNOWLEDGE.md
│   ├── NEGATIVE_KNOWLEDGE.md
│   ├── KNOWLEDGE_PROMOTION.md
│   └── CONTINUOUS_LEARNING.md
└── memory/
    ├── EXECUTIONS.md
    ├── LESSONS.md
    ├── FAILURES.md
    └── PATTERNS.md
```

## Usage

1. Choose `language` (pt-BR | en-US), `target_age` (6–8), `style`, and `engine`.
2. Start from `templates/parameter_defaults.md` and apply style modifiers.
3. Produce a `voice_params.json` (see `templates/example_voice_params.json`).
4. Validate:

```bash
python scripts/validate_profile.py voice_params.json
```

5. Map the generic parameters onto your engine's controls and verify by
   listening. Adjust and re-validate.

## Open-source engines

- **Coqui TTS / XTTS v2** — `templates/engine_coqui_xtts.md` (multilingual pt/en,
  style/speed control, runs local).
- **Piper** — `templates/engine_piper.md` (offline, lightweight; limited native
  control).
- **Post-processing** — `templates/post_processing.md` maps formant/VTL shift,
  fine pitch, EQ and dynamics onto rubberband/librosa/SoX, since the engines do
  not expose these natively.

Do not use a real identifiable child's recording as an engine style reference.

## Consent gate

If real recordings of minors inform tuning, a **consent reference (pointer
only)** is required — see `templates/consent_gate.md`. Never store recording
content, transcripts, personal data, or voiceprints.

## Tests

```bash
python tests/test_validate_profile.py
```
