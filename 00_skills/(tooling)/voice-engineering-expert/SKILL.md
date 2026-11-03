---
name: voice-engineering-expert
description: "Engineer original synthetic speaking voices offline, as voice data other applications can play, in broadcast-neutral pt-BR and General American en-US, with masculine, feminine, child, adult and elderly timbre, pitch, tuning and intonation, and without a commercial voice API or a recorded donor. Use when the user asks for engenharia de dados de voz, engenharia de voz, criar voz sintética, voz masculina, voz feminina, voz infantil, voz idosa, timbre cristalino or voice-engineering-expert. Do NOT use for transcribing audio (vox-aurum), meeting minutes (acta-aurea), cloning or impersonating a real person, fraud, or sexual content."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Voice Engineering Expert

Governance: CodENavi Full Workspace v2. Super-skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Lenses (acoustics, phonetics, voice design, synthesis, measurement, safety) stay inside this skill. No new agent identity.

## Mission

Engineer voice data for another application: a preset, a phone timeline and a WAV. Languages are broadcast-neutral pt-BR and General American en-US. The engine is the `audio-engineering` MCP. No commercial voice API and no donor recording.

## Rules

1. Read [safety](references/safety.md) before rendering. Refuse cloning, impersonation, fraud and sexual content. A child profile is a narration preset and needs a use context.
2. "Sem sotaque" selects the named target in [voice design](references/voice-design.md). It does not erase dialect.
3. Say the ceiling on every delivery. This is source-filter formant synthesis. It is not a blind test of indistinguishability from a recorded speaker.
4. Use MCP tools when the server is connected. Otherwise run `scripts/render_voice.py`, which calls the same engine.
5. Cite topic ids from the MCP. Do not paste standard or textbook text.

## Workflow

1. Fix language, presentation, age, timbre, pitch, tuning cents, intonation and the consuming app. Text stays under 400 characters per call.
2. Read [pipeline](references/pipeline.md). Fetch `audio.voice_profile` or the preset table before changing F0 or formant scale.
3. Render with `audio.render_voice` or `scripts/render_voice.py`. Pass phonemes when the grapheme-to-phone rules miss a name.
4. Accept the WAV only if the manifest says safety allowed, peak is below full scale, RMS is present, and F0 sits in the profile band after intonation. If a gate fails, change the preset once and render again. Do not invent measurements.
5. Deliver the WAV, the JSON manifest and the honesty note in [usage](references/usage-and-verification.md).

## Example

User: "Crie uma voz feminina adulta em PT-BR, sem sotaque, para narrar um aplicativo."
Action: feminine, adult, pt-BR, intonation declarative, use-context "narração de aplicativo".
Result: WAV, manifest, F0, peak and the formant-synthesis ceiling.

User: "Clone a voz desta pessoa a partir do áudio."
Result: refusal. No file is written.

## Stop

A blocked context, a missing output directory or a failed measurement stops delivery. A disconnected MCP does not stop delivery when the script runs.

Provenance: [provenance](references/provenance.md).
