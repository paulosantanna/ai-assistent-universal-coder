"""Reference phone inventory for the parametric voice engine.

Formant numbers are masculine-adult engineering targets in hertz, rounded for
synthesis. They are not a copied vowel table. Feminine, child and older
profiles scale them at render time. Bandwidths are applied by the synthesizer.
"""

# kind: vowel, nasal, liquid, glide, fricative, vfricative, stop, tap, silence
PHONES = {
    "a": {"kind": "vowel", "f": (730, 1250, 2500), "ms": 110},
    "e": {"kind": "vowel", "f": (400, 2000, 2650), "ms": 95},
    "E": {"kind": "vowel", "f": (590, 1780, 2550), "ms": 100},
    "i": {"kind": "vowel", "f": (280, 2280, 3000), "ms": 90},
    "o": {"kind": "vowel", "f": (420, 860, 2500), "ms": 95},
    "O": {"kind": "vowel", "f": (580, 1020, 2500), "ms": 100},
    "u": {"kind": "vowel", "f": (310, 780, 2350), "ms": 90},
    "ax": {"kind": "vowel", "f": (500, 1500, 2500), "ms": 70},
    "a~": {"kind": "nasal", "f": (680, 1200, 2400), "ms": 120},
    "e~": {"kind": "nasal", "f": (430, 1750, 2500), "ms": 110},
    "i~": {"kind": "nasal", "f": (320, 2050, 2750), "ms": 100},
    "o~": {"kind": "nasal", "f": (460, 900, 2350), "ms": 110},
    "u~": {"kind": "nasal", "f": (340, 820, 2250), "ms": 100},
    "j": {"kind": "glide", "f": (320, 2100, 2900), "ms": 55},
    "w": {"kind": "glide", "f": (360, 760, 2300), "ms": 55},
    "l": {"kind": "liquid", "f": (400, 1200, 2600), "ms": 60},
    "lh": {"kind": "liquid", "f": (360, 1900, 2800), "ms": 70},
    "tap": {"kind": "tap", "f": (450, 1500, 2500), "ms": 28},
    "r": {"kind": "liquid", "f": (420, 1060, 1580), "ms": 70},
    "m": {"kind": "nasal", "f": (280, 1200, 2300), "ms": 70},
    "n": {"kind": "nasal", "f": (300, 1500, 2500), "ms": 70},
    "nh": {"kind": "nasal", "f": (320, 1900, 2700), "ms": 75},
    "p": {"kind": "stop", "burst": 1400, "ms": 55, "voice_bar": False},
    "b": {"kind": "stop", "burst": 1100, "ms": 50, "voice_bar": True},
    "t": {"kind": "stop", "burst": 2200, "ms": 50, "voice_bar": False},
    "d": {"kind": "stop", "burst": 1900, "ms": 48, "voice_bar": True},
    "k": {"kind": "stop", "burst": 1800, "ms": 60, "voice_bar": False},
    "g": {"kind": "stop", "burst": 1600, "ms": 55, "voice_bar": True},
    "f": {"kind": "fricative", "nfreq": 1700, "nbw": 1400, "ms": 90, "noise": 0.22},
    "v": {"kind": "vfricative", "f": (350, 1400, 2500), "nfreq": 1600, "nbw": 1200, "ms": 80, "noise": 0.12},
    "s": {"kind": "fricative", "nfreq": 6200, "nbw": 2200, "ms": 100, "noise": 0.16},
    "z": {"kind": "vfricative", "f": (320, 1600, 2600), "nfreq": 5600, "nbw": 2000, "ms": 90, "noise": 0.10},
    "sh": {"kind": "fricative", "nfreq": 3200, "nbw": 1600, "ms": 100, "noise": 0.18},
    "zh": {"kind": "vfricative", "f": (340, 1600, 2500), "nfreq": 3000, "nbw": 1400, "ms": 90, "noise": 0.11},
    "h": {"kind": "fricative", "nfreq": 1400, "nbw": 1800, "ms": 70, "noise": 0.14},
    "th": {"kind": "fricative", "nfreq": 5500, "nbw": 3000, "ms": 80, "noise": 0.10},
    "dh": {"kind": "vfricative", "f": (350, 1400, 2500), "nfreq": 1800, "nbw": 1600, "ms": 60, "noise": 0.08},
    "tsh": {"kind": "affricate", "burst": 2800, "nfreq": 4200, "nbw": 1800, "ms": 95, "noise": 0.16, "voice_bar": False},
    "dzh": {"kind": "affricate", "burst": 2400, "nfreq": 3800, "nbw": 1600, "ms": 90, "noise": 0.12, "voice_bar": True},
    "sil": {"kind": "silence", "ms": 90},
}

VOWEL_PHONES = {
    "a", "e", "E", "i", "o", "O", "u", "ax",
    "a~", "e~", "i~", "o~", "u~",
}

PRESETS = {
    ("masculine", "adult"): {
        "f0_hz": 118, "formant_scale": 1.00, "tilt": 0.96, "jitter": 0.006,
        "shimmer": 0.04, "breath": 0.035, "open_quotient": 0.56, "clarity": 0.42,
    },
    ("feminine", "adult"): {
        "f0_hz": 206, "formant_scale": 1.17, "tilt": 0.90, "jitter": 0.007,
        "shimmer": 0.045, "breath": 0.07, "open_quotient": 0.62, "clarity": 0.50,
    },
    ("masculine", "child"): {
        "f0_hz": 268, "formant_scale": 1.38, "tilt": 0.86, "jitter": 0.008,
        "shimmer": 0.05, "breath": 0.04, "open_quotient": 0.60, "clarity": 0.55,
    },
    ("feminine", "child"): {
        "f0_hz": 286, "formant_scale": 1.42, "tilt": 0.85, "jitter": 0.008,
        "shimmer": 0.05, "breath": 0.045, "open_quotient": 0.60, "clarity": 0.55,
    },
    ("masculine", "older"): {
        "f0_hz": 138, "formant_scale": 1.02, "tilt": 0.93, "jitter": 0.018,
        "shimmer": 0.09, "breath": 0.14, "open_quotient": 0.70, "clarity": 0.36,
    },
    ("feminine", "older"): {
        "f0_hz": 180, "formant_scale": 1.14, "tilt": 0.88, "jitter": 0.016,
        "shimmer": 0.08, "breath": 0.15, "open_quotient": 0.70, "clarity": 0.40,
    },
}

PRESENTATIONS = ("masculine", "feminine")
AGES = ("child", "adult", "older")
LANGUAGES = ("pt-BR", "en-US")
ACCENT_TARGETS = {
    "pt-BR": "pt-BR-broadcast",
    "en-US": "en-US-general-american",
}
