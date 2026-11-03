# Voice design

Presets live in `audio-engineering-mcp/phones.py`. Numbers are engineering targets grounded in the MCP topics `f0-age-presentation`, `pt-br-phonetics` and `en-us-phonetics`, not a copied vowel table.

| Presentation | Age | F0 Hz | Formant scale | Character |
| --- | --- | --- | --- | --- |
| masculine | adult | 118 | 1.00 | reference tract |
| feminine | adult | 206 | 1.17 | about 1.7 times F0, shorter tract |
| masculine | child | 268 | 1.38 | higher F0 and formants |
| feminine | child | 286 | 1.42 | higher F0 and formants |
| masculine | older | 138 | 1.02 | more jitter, shimmer and breath |
| feminine | older | 180 | 1.14 | more jitter, shimmer and breath |

## Controls

- Timbre: `brightness` 0 to 0.85 and `breath` 0 to 0.45. Brightness is the clarity mix. Breath is aspiration in the source.
- Pitch: `f0_hz` replaces the preset reference.
- Tuning: `tuning_cents` shifts that reference. 100 cents is one semitone. A4 is 440 Hz when a note is calculated with `audio.calculate`.
- Intonation: `auto` follows punctuation, `declarative` falls, `question` rises, `narrow` stays small, `flat` holds the reference. The manifest F0 target is the reference before the contour.
- Rate: 0.75 to 1.4, where 1 is the preset duration.

## Accent targets

- pt-BR selects `pt-BR-broadcast`: careful vowels, unstressed final e/o reduced, ti/di affricated, coda s not palatalized, coda l vocalized, strong r as a glottal fricative, single r as a tap.
- en-US selects `en-US-general-american`: rhotic r with a low third formant and reduced vowels as schwa.
- Pass `affricate_ti=false` on the script for a less affricated Portuguese reading.
- Pass `--phonemes` when a proper name needs a fixed pronunciation. Symbols are the keys of the phone inventory, space-separated.

F0 reported on a full sentence can sit above the reference because the contour and intrinsic vowel pitch move it. Judge a flat sustained vowel when the question is whether the preset itself is in band.
