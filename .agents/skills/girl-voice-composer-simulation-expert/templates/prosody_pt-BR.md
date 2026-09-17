# Prosody & pronunciation direction — pt-BR (generic female child, age 6-8)

Generic direction for a fictional young-girl voice in Brazilian Portuguese.
These are directorial guidelines, not measurements of any real person.

## Intonation / entoação
- Contours are more lively and variable than adult speech; frequent gentle
  rises, especially in questions and enumerations.
- Declaratives end with a soft fall; keep the fall shallow to preserve a light,
  childlike quality.
- Storytelling style: exaggerate pitch excursions on key words; keep them
  natural, not cartoonish.

## Rhythm / ritmo silábico
- Brazilian Portuguese is syllable-timed: give syllables fairly even duration.
- Youngest end (6): slightly slower, clearer syllable separation.
- Age 8: more fluent, connected timing.
- Micro-pauses at clause boundaries (commas, clause breaks) preserve coherence
  and avoid run-on delivery.

## Pronunciation cues
- Clear open vowels; avoid heavy vowel reduction.
- Watch nasal vowels (ão, ãe, õe) and palatals (lh, nh) — keep them crisp but
  soft.
- Avoid adult-style strong coarticulation that erases the childlike clarity.

## Common tuning notes
- If the engine sounds too adult: raise pitch mean and formant (VTL) shift.
- If it sounds robotic: raise `prosody.pitch_variability` and `rhythm.pause_bias`.
- If sibilance is harsh on "s"/"ch": apply `eq.sibilance_control_db`.
