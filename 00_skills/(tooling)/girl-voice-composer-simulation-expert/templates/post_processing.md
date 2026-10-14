# Post-processing chain (open source) — pitch, formants, EQ, dynamics

Neither Coqui XTTS nor Piper expose formant/VTL shifting, fine pitch targeting,
or a full EQ. Achieve those from the skill's parameters with open-source audio
tools applied to the engine's raw output.

Tools (all open source):
- **rubberband** (GPL) — high-quality pitch + formant shifting.
- **librosa** (ISC) + **pyrubberband** — Python pipeline.
- **SoX** (GPL/LGPL) or **ffmpeg** (LGPL/GPL) — EQ, compression, de-essing.

> Order matters. Recommended chain:
> raw -> formant/VTL shift -> pitch shift -> EQ -> de-ess -> gentle compression.

## 1. Formant / VTL shift  (from formants.vtl_shift_semitones)

Shorter child vocal tract => shift formants up. With rubberband CLI:

```bash
# shift formants up by S semitones while keeping pitch (approx via -F/--formant)
rubberband --formant --pitch 0 -c 5 in.wav formant.wav
```

With pyrubberband (finer control):
```python
import soundfile as sf, pyrubberband as pyrb
y, sr = sf.read("raw.wav")
# vtl_shift_semitones from profile; positive = up
y2 = pyrb.pitch_shift(y, sr, n_steps=0, rbargs={"--formant": ""})
```
(Set the formant amount to match `vtl_shift_semitones`; verify by listening.)

## 2. Pitch shift  (from pitch.mean_f0_hz)

Measure the raw mean f0 (e.g. librosa.pyin) and shift to the target:

```python
import librosa, numpy as np, soundfile as sf, pyrubberband as pyrb
y, sr = sf.read("formant.wav")
f0, vflag, _ = librosa.pyin(y, fmin=80, fmax=600, sr=sr)
raw_mean = float(np.nanmedian(f0))
target = 290.0  # profile.pitch.mean_f0_hz
n_steps = 12 * np.log2(target / raw_mean)
y2 = pyrb.pitch_shift(y, sr, n_steps=n_steps)
sf.write("pitched.wav", y2, sr)
```
Keep the result within [min_f0_hz, max_f0_hz]; avoid the "chipmunk" artifact by
pairing pitch with the formant shift in step 1.

## 3. EQ  (from eq.*)  — SoX example

```bash
sox pitched.wav eq.wav \
  bass  -4 120 \                 # low_shelf_db @ ~120 Hz
  treble +3 4000 \               # presence_boost_db @ ~4 kHz
  equalizer 7000 2q -3           # sibilance_control_db @ ~7 kHz (de-ess region)
```

## 4. De-ess + gentle compression  (from dynamics.*)

```bash
sox eq.wav final.wav \
  compand 0.1,0.2 -60,-40,-30,-15 -3   # light compression (map from dynamics.compression)
```
Keep compression light (childlike liveliness); breathiness comes mostly from
the engine/reference, not post-processing.

## Validate the profile first
Always run `python scripts/validate_profile.py voice_params.json` before
rendering, so the target values are in range.
