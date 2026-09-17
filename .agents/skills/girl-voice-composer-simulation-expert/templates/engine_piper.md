# Engine mapping — Piper (open source)

Piper is a fast, fully offline neural TTS. It exposes very few acoustic
controls, so most of the skill's parameters are achieved in post-processing.

- Repo: https://github.com/rhasspy/piper  (MIT)
- Voices: per-language ONNX voices, incl. `pt_BR` and `en_US`.
- Great for lightweight/offline; limited native acoustic control.

> Safety: pick a GENERIC published voice model; do not attempt to reproduce a
> specific real child. See `templates/consent_gate.md` and SKILL.md §4/§14.

## What Piper exposes natively (map these)

| Generic param              | Piper control    | Notes |
|----------------------------|------------------|-------|
| language                   | voice model file | choose a `pt_BR` or `en_US` child/female voice model |
| rhythm.speech_rate_wpm     | `--length-scale` | >1.0 slower, <1.0 faster (inverse of speed) |
| prosody.pitch_variability  | `--noise-scale`  | more variation in prosody/timbre |
| micro-timing variation     | `--noise-w`      | phoneme duration variation |
| rhythm.pause_bias          | `--sentence-silence` | seconds of silence between sentences |

`length_scale` suggestion (baseline adult ~= 150 wpm):
`length_scale = clamp(150.0 / speech_rate_wpm, 0.7, 1.6)`

## What Piper does NOT expose (do in post-processing)

- `pitch.*`               -> pitch shift
- `formants.vtl_shift_semitones` -> formant shift
- `eq.*`                  -> SoX/ffmpeg EQ
- `dynamics.*`            -> light compression

## Minimal example (CLI, illustrative)

```bash
echo "Once upon a time there was a curious girl..." | \
  piper --model en_US-child.onnx \
        --length-scale 1.23 \      # 150/122
        --noise-scale 0.8 \        # from pitch_variability
        --sentence-silence 0.55 \  # from pause_bias
        --output_file raw.wav
# then apply post_processing.md chain (pitch/formant/EQ) -> final.wav
```

Fill `engine.controls` in the profile like:
```json
"engine": {
  "id": "piper",
  "mapping_mode": "mapped",
  "controls": {
    "language": "model",
    "rhythm.speech_rate_wpm": "--length-scale",
    "prosody.pitch_variability": "--noise-scale",
    "rhythm.pause_bias": "--sentence-silence"
  }
}
```
