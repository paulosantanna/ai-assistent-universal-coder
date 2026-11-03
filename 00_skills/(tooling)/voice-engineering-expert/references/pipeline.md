# Pipeline

## MCP path

When `audio-engineering` is connected:

1. `audio.health` confirms the corpus and the ceiling.
2. `audio.topic` or `audio.search` answers an engineering question. Prefer topic ids over memory.
3. `audio.voice_profile` returns the preset.
4. `audio.calculate` evaluates nyquist, wavelength, sabine, eyring, erb, cents or note.
5. `audio.render_voice` writes WAV and JSON. `out_dir` must stay under the working directory or `/tmp`.

## Script path

From the repository root:

```bash
python3 "00_skills/(tooling)/voice-engineering-expert/scripts/render_voice.py" \
  --text "Olá, eu sou uma voz sintética." \
  --language pt-BR --presentation feminine --age adult \
  --intonation declarative --use-context "narração de aplicativo" \
  --out-dir /tmp/voice-render
```

Optional flags: `--tuning-cents`, `--f0-hz`, `--brightness`, `--breath`, `--formant-scale`, `--rate`, `--phonemes`, `--no-affricate`.

## What another application receives

- WAV, PCM, 22050 Hz, 16-bit, mono, dithered, peak below full scale.
- JSON manifest with profile, phones, intonation, measurements, safety, seed and `ceiling`.
- No SDK and no account. The application plays the WAV or encodes it later. Opus is a delivery codec, not the master. See MCP topic `codecs-opus`.

## Verification command

```bash
python3 "00_skills/(tooling)/voice-engineering-expert/scripts/self_check.py"
```

The check renders six presets, one Portuguese sentence, one English sentence, the safety refusals, the formula helpers and a stdio handshake against the MCP.
