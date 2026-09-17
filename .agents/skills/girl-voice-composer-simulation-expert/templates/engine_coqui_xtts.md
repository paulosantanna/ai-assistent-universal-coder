# Engine mapping — Coqui TTS / XTTS v2 (open source)

Maps the skill's generic acoustic parameters onto Coqui TTS controls, plus the
post-processing chain for what XTTS does not expose natively.

- Repo: https://github.com/coqui-ai/TTS  (Mozilla-lineage, MPL-2.0)
- Model: `tts_models/multilingual/multi-dataset/xtts_v2` (supports `pt`, `en`)
- Runs locally (GPU recommended; CPU works, slower).

> Safety: this skill generates a **generic, fictional** child voice. Do NOT feed
> a real identifiable child's recording as the XTTS `speaker_wav` reference to
> imitate that person. Use a synthetic/consented generic reference only. See
> `templates/consent_gate.md` and SKILL.md §4/§14.

## What XTTS exposes natively (map these)

| Generic param            | XTTS control                        | Notes |
|--------------------------|-------------------------------------|-------|
| language                 | `language` (`pt`, `en`)             | pt-BR -> `pt`, en-US -> `en` |
| rhythm.speech_rate_wpm   | `speed`                             | ~1.0 = baseline; scale relative to a reference adult rate |
| style / prosody          | `speaker_wav` (reference style)     | Use a GENERIC/synthetic reference, never a real child |
| prosody.pitch_variability| `temperature` (indirect)            | Higher temperature = more expressive/variable; verify |
| coherence/stability      | `repetition_penalty`, `length_penalty` | Reduce run-ons / repetition |

`speed` mapping suggestion (baseline adult ~= 150 wpm):
`speed = clamp(speech_rate_wpm / 150.0, 0.6, 1.4)`

## What XTTS does NOT expose (do in post-processing)

- `pitch.mean_f0_hz` / min / max  -> pitch shift (see post_processing.md)
- `formants.vtl_shift_semitones`  -> formant shift (rubberband/librosa)
- `eq.*`                          -> SoX/ffmpeg EQ
- `dynamics.breathiness/compression` -> light compression / avoid over-comp

## Minimal example (Python, illustrative)

```python
from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
tts.tts_to_file(
    text="Era uma vez uma menina curiosa...",
    file_path="raw.wav",
    language="pt",                 # from profile.language
    speaker_wav="generic_ref.wav", # GENERIC/consented reference only
    speed=0.81,                    # 122 wpm / 150
)
# then apply post_processing.md chain (pitch/formant/EQ) -> final.wav
```

Fill `engine.controls` in the profile like:
```json
"engine": {
  "id": "coqui-xtts-v2",
  "mapping_mode": "mapped",
  "controls": {
    "language": "language",
    "rhythm.speech_rate_wpm": "speed",
    "prosody.pitch_variability": "temperature",
    "style": "speaker_wav"
  }
}
```
