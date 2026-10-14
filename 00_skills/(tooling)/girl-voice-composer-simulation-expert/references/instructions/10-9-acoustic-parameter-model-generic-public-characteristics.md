<!-- Package: 00_skills/(tooling)/girl-voice-composer-simulation-expert; relative command/resource examples resolve from that package or workspace root. -->

## 9. Acoustic parameter model (generic, public characteristics)

These are **generic ranges** describing typical female child speech in the 6–8
band, drawn from general phonetics/acoustics knowledge. They are starting
points to be tuned per engine and per utterance — not measurements of any
individual, and not guaranteed values. Treat all ranges as approximate.

- **Fundamental frequency (pitch, f0).** Children 6–8 typically sit noticeably
  higher than adults. Use a working **mean f0 in the ~250–320 Hz** region as a
  starting band, with expressive excursions above and below. Tune to taste and
  to engine behavior; verify by listening.
- **Formants.** Child vocal tracts are shorter, so formants are scaled upward
  relative to adults. Apply an upward **formant shift / vocal-tract-length
  scaling** where the engine exposes it (a modest positive shift), rather than
  fixed absolute values, since formants are vowel-dependent.
- **Prosody / intonation.** Wider pitch variability, more frequent rises,
  lively contours for cheerful/storytelling styles; flatter contours for
  calm/neutral.
- **Syllable rhythm / rate.** Slightly slower and more evenly timed than fluent
  adults for the youngest end (6), moving toward more fluent timing by 8.
  Insert natural micro-pauses at clause boundaries to preserve coherence.
- **EQ / spectral balance.** Gentle presence lift in the upper-mid region for
  intelligibility; avoid harsh sibilance; keep low end light (small voices have
  limited low-frequency energy). Exact bands depend on the engine's EQ surface.
- **Dynamics / quality.** Breathier, lighter phonation than adults; avoid
  over-compression that flattens the childlike liveliness.

Language specifics are in `templates/prosody_pt-BR.md` and
`templates/prosody_en-US.md`.

The concrete numeric defaults live in `schemas/voice_profile.schema.json` and
`templates/parameter_defaults.md`, so validation stays deterministic.

### Reference open-source engine mappings

- `templates/engine_coqui_xtts.md` — Coqui TTS / XTTS v2 (multilingual pt/en).
- `templates/engine_piper.md` — Piper (offline, lightweight).
- `templates/post_processing.md` — open-source chain (rubberband/librosa/SoX)
  for parameters the engines do not expose natively (formant/VTL shift, fine
  pitch targeting, EQ, dynamics).

---
