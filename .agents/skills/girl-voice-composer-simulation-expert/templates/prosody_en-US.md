# Prosody & pronunciation direction — en-US (generic female child, age 6-8)

Generic direction for a fictional young-girl voice in American English.
These are directorial guidelines, not measurements of any real person.

## Intonation
- Lively, variable contours; more frequent rises than adult speech.
- Declaratives fall gently; questions rise clearly.
- Storytelling style: broader pitch range on emphasized words; keep natural.

## Rhythm
- American English is stress-timed: keep clear stress on content words and
  reduce function words, but less aggressively than a fluent adult (children
  reduce less).
- Youngest end (6): slightly slower, more deliberate; age 8 more fluent.
- Insert micro-pauses at clause boundaries to preserve coherence.

## Pronunciation cues
- Keep vowels bright; avoid over-reduced schwa that reads as adult.
- Rhotic "r" present but light.
- Avoid harsh sibilance on "s"/"sh".

## Common tuning notes
- Too adult -> raise pitch mean and formant (VTL) shift.
- Too robotic -> raise `prosody.pitch_variability` and `rhythm.pause_bias`.
- Harsh sibilance -> apply `eq.sibilance_control_db`.
