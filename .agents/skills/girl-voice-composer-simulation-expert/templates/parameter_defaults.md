# Parameter defaults by age point (generic, fictional child voice)

Starting points only. Tune per engine and verify by listening. These are
generic approximations of typical female child speech, not measurements of any
individual, and carry no guarantee.

| Parameter                 | Age 6      | Age 7      | Age 8      |
|---------------------------|------------|------------|------------|
| pitch.mean_f0_hz          | ~300       | ~290       | ~275       |
| pitch.min_f0_hz           | ~230       | ~225       | ~215       |
| pitch.max_f0_hz           | ~430       | ~420       | ~400       |
| formants.vtl_shift_semis  | ~3.5       | ~3.0       | ~2.5       |
| prosody.pitch_variability | 0.70       | 0.65       | 0.60       |
| prosody.contour           | lively     | lively     | moderate   |
| rhythm.speech_rate_wpm    | ~110       | ~125       | ~140       |
| rhythm.pause_bias         | 0.55       | 0.50       | 0.45       |
| eq.low_shelf_db           | -4         | -4         | -3         |
| eq.presence_boost_db      | 3          | 3          | 2.5        |
| eq.sibilance_control_db   | -3         | -3         | -3         |
| dynamics.breathiness      | 0.55       | 0.50       | 0.45       |
| dynamics.compression      | 0.25       | 0.30       | 0.30       |

## Style modifiers (add on top of the age baseline)

- cheerful: +0.10 pitch_variability, contour -> lively, +5 wpm
- storytelling: +0.15 pitch_variability, contour -> lively, +0.05 pause_bias
- calm: -0.15 pitch_variability, contour -> moderate/flat, -10 wpm
- neutral: no change
