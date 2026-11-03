"""Source-filter formant synthesizer.

The glottal flow uses a Rosenberg-style open phase plus a short closing phase.
The vocal tract is a cascade of two-pole resonators. Frication is parallel
noise through one resonator. No recorded voice and no neural vocoder is used.

The output is intelligible parametric speech with controllable pitch, scale,
breath and intonation. It is not a claim that a listener cannot tell it from
a recorded human.
"""
import hashlib
import math
import random

from g2p import parse_phone_string, text_to_phones
from measure import hz_from_cents, signal_metrics
from phones import ACCENT_TARGETS, AGES, LANGUAGES, PHONES, PRESETS, PRESENTATIONS, VOWEL_PHONES
from safety import assert_allowed

SR = 22050
MAX_SECONDS = 18
CEILING = (
    "parametric-formant: original source-filter speech, not a blind-test claim "
    "of indistinguishability from a recorded speaker"
)
VOICED_KINDS = {"vowel", "nasal", "liquid", "glide", "tap", "vfricative", "closure"}


def synthesize(
    text,
    language="pt-BR",
    presentation="feminine",
    age="adult",
    intonation="auto",
    tuning_cents=0,
    f0_hz=None,
    brightness=None,
    breath=None,
    formant_scale=None,
    rate=1.0,
    phonemes=None,
    affricate_ti=True,
    use_context="",
    extra=None,
    seed=None,
):
    if language not in LANGUAGES:
        raise ValueError("language must be pt-BR or en-US")
    decision = assert_allowed(text, use_context, presentation, age, extra)
    if phonemes:
        phones = parse_phone_string(phonemes)
        question = bool(text.strip().endswith("?"))
    else:
        if not str(text or "").strip():
            raise ValueError("text is empty")
        parsed = text_to_phones(text, language, affricate_ti=affricate_ti)
        phones = parsed["phones"]
        question = parsed["question"]
    contour = intonation
    if contour == "auto":
        contour = "question" if question else "declarative"
    if contour not in ("declarative", "question", "narrow", "flat"):
        raise ValueError("unknown intonation")
    profile = resolve_profile(presentation, age, tuning_cents, f0_hz, brightness, breath, formant_scale)
    segments = build_segments(phones, rate, contour)
    key = "|".join([
        text or "", phonemes or "", language, presentation, age, contour,
        str(profile["f0_hz"]), str(profile["formant_scale"]), str(rate),
    ])
    chosen = seed if seed is not None else int(hashlib.sha256(key.encode("utf-8")).hexdigest()[:8], 16)
    samples = render_segments(segments, profile, chosen)
    metrics = signal_metrics(samples, SR)
    metrics["f0_target_hz"] = profile["f0_hz"]
    return {
        "samples": samples,
        "sample_rate": SR,
        "profile": public_profile(profile, presentation, age, language),
        "accent_target": ACCENT_TARGETS[language],
        "phones": [phone for phone, _stress in phones],
        "intonation": contour,
        "measurements": metrics,
        "safety": decision,
        "ceiling": CEILING,
        "seed": chosen,
    }


def resolve_profile(presentation, age, tuning_cents, f0_hz, brightness, breath, formant_scale):
    if (presentation, age) not in PRESETS:
        raise ValueError("unknown voice preset")
    profile = dict(PRESETS[(presentation, age)])
    if f0_hz is not None:
        profile["f0_hz"] = float(f0_hz)
    if tuning_cents:
        profile["f0_hz"] = hz_from_cents(profile["f0_hz"], tuning_cents)
    if formant_scale is not None:
        profile["formant_scale"] = float(formant_scale)
    if breath is not None:
        profile["breath"] = float(breath)
    if brightness is not None:
        profile["clarity"] = float(brightness)
    profile["f0_hz"] = _clamp(profile["f0_hz"], 75, 460)
    profile["formant_scale"] = _clamp(profile["formant_scale"], 0.85, 1.65)
    profile["breath"] = _clamp(profile["breath"], 0.0, 0.45)
    profile["clarity"] = _clamp(profile["clarity"], 0.0, 0.85)
    profile["jitter"] = _clamp(profile["jitter"], 0.0, 0.05)
    profile["shimmer"] = _clamp(profile["shimmer"], 0.0, 0.2)
    profile["open_quotient"] = _clamp(profile["open_quotient"], 0.35, 0.8)
    profile["tilt"] = _clamp(profile["tilt"], 0.5, 0.98)
    return profile


def public_profile(profile, presentation, age, language):
    data = dict(profile)
    data.update({
        "presentation": presentation,
        "age": age,
        "language": language,
        "accent_target": ACCENT_TARGETS[language],
    })
    return data


def build_segments(phones, rate, contour):
    speed = _clamp(float(rate), 0.75, 1.4)
    segments = []
    for phone, stress in phones:
        spec = PHONES[phone]
        kind = spec["kind"]
        dur = spec["ms"] / 1000.0
        if stress and phone in VOWEL_PHONES:
            dur *= 1.42
        elif phone in VOWEL_PHONES:
            dur *= 0.88
        dur /= speed
        formants = spec.get("f")
        if kind in ("vowel", "nasal", "liquid", "glide", "tap"):
            segments.append(_voiced(phone, kind, dur, formants, 1.0 if kind == "vowel" else 0.72, stress))
        elif kind == "fricative":
            segments.append(_noise(phone, dur, spec["nfreq"], spec["nbw"], spec["noise"], False))
        elif kind == "vfricative":
            segments.append(_voiced(phone, kind, dur, formants, 0.55, stress, spec["nfreq"], spec["nbw"], spec["noise"]))
        elif kind == "stop":
            closed = dur * 0.78
            segments.append(_closure(phone, closed, spec["voice_bar"]))
            segments.append(_noise(phone, 0.012, spec["burst"], 900, 0.28, False, kind="burst"))
        elif kind == "affricate":
            segments.append(_closure(phone, 0.028, spec["voice_bar"]))
            segments.append(_noise(phone, max(0.04, dur - 0.028), spec["nfreq"], spec["nbw"], spec["noise"], spec["voice_bar"]))
        else:
            segments.append({"phone": "sil", "kind": "silence", "dur": dur, "voiced": False, "f0_mul": 1.0, "noise": 0.0, "amp": 0.0})
    _apply_contour(segments, contour)
    return segments


def _voiced(phone, kind, dur, formants, amp, stress, nfreq=0.0, nbw=800.0, noise=0.0):
    return {
        "phone": phone, "kind": kind, "dur": dur, "f": formants, "amp": amp,
        "voiced": True, "stress": stress, "f0_mul": 1.0, "noise": noise,
        "nfreq": nfreq, "nbw": nbw,
    }


def _noise(phone, dur, nfreq, nbw, noise, voiced, kind="fricative"):
    return {
        "phone": phone, "kind": kind, "dur": dur, "f": None, "amp": noise,
        "voiced": voiced, "stress": False, "f0_mul": 1.0, "noise": noise,
        "nfreq": nfreq, "nbw": nbw,
    }


def _closure(phone, dur, voice_bar):
    return {
        "phone": phone, "kind": "closure", "dur": dur,
        "f": (320, 1100, 2300), "amp": 0.18 if voice_bar else 0.0,
        "voiced": voice_bar, "stress": False, "f0_mul": 0.92, "noise": 0.0,
        "nfreq": 0.0, "nbw": 400.0,
    }


def _apply_contour(segments, contour):
    voiced = [index for index, seg in enumerate(segments) if seg["voiced"] and seg["kind"] != "closure"]
    total = len(voiced)
    for order, index in enumerate(voiced):
        position = order / (total - 1) if total > 1 else 0.0
        if contour == "question":
            multiplier = 0.96 + 0.42 * position
        elif contour == "narrow":
            multiplier = 1.0 + 0.05 * math.sin(position * math.pi)
        elif contour == "flat":
            multiplier = 1.0
        else:
            multiplier = 1.14 - 0.36 * position
        if segments[index].get("stress"):
            multiplier *= 1.08
        phone = segments[index]["phone"]
        if phone in ("i", "u", "i~", "u~"):
            multiplier *= 1.035
        if phone in ("a", "a~"):
            multiplier *= 0.98
        segments[index]["f0_mul"] = multiplier


def render_segments(segments, profile, seed):
    counts = [max(0, int(seg["dur"] * SR)) for seg in segments]
    total = sum(counts)
    if total <= 0:
        raise ValueError("empty audio")
    if total > SR * MAX_SECONDS:
        raise ValueError("utterance longer than 18 seconds; split the text")
    rng = random.Random(seed)
    scale = profile["formant_scale"]
    output = [0.0] * total
    state = [(0.0, 0.0) for _ in range(6)]
    coeff = [(0.0, -0.95) for _ in range(6)]

    def configure(index, freq, bandwidth):
        freq = min(max(90.0, freq), SR * 0.45)
        bandwidth = max(50.0, bandwidth)
        radius = math.exp(-math.pi * bandwidth / SR)
        theta = 2.0 * math.pi * freq / SR
        coeff[index] = (2.0 * radius * math.cos(theta), -radius * radius)

    def resonate(index, excitation):
        previous, older = state[index]
        first, second = coeff[index]
        current = excitation + first * previous + second * older
        if current > 1e7 or current < -1e7:
            current = 0.0
            previous = 0.0
        state[index] = (current, previous)
        return current

    f0_base = profile["f0_hz"]
    jitter = profile["jitter"]
    shimmer = profile["shimmer"]
    breath = profile["breath"]
    tilt = profile["tilt"]
    open_quotient = profile["open_quotient"]
    clarity = profile["clarity"]
    cursor = 0
    previous_formants = None
    period = max(8, int(SR / f0_base))
    phase = period
    previous_flow = 0.0
    pulse_amp = 1.0
    tilt_state = 0.0
    previous_tract = 0.0

    for seg, count in zip(segments, counts):
        kind = seg["kind"]
        for step in range(count):
            formants = seg.get("f")
            if formants and previous_formants and step < count * 0.3:
                mix = step / max(1.0, count * 0.3)
                formants = tuple(previous_formants[axis] + (formants[axis] - previous_formants[axis]) * mix for axis in range(3))
            f0 = _clamp(f0_base * seg.get("f0_mul", 1.0), 70, 480)
            excitation = 0.0
            if seg["voiced"]:
                if phase >= period:
                    period = max(8, int((SR / f0) * (1.0 + jitter * ((rng.random() * 2.0) - 1.0))))
                    pulse_amp = 1.0 + shimmer * ((rng.random() * 2.0) - 1.0)
                    phase = 0
                    previous_flow = 0.0
                open_samples = max(4, int(open_quotient * period))
                close_samples = max(3, int(0.16 * period))
                if phase < open_samples:
                    flow = 0.5 * (1.0 - math.cos(math.pi * phase / open_samples))
                elif phase < open_samples + close_samples:
                    flow = math.cos(0.5 * math.pi * (phase - open_samples) / close_samples)
                else:
                    flow = 0.0
                derivative = (flow - previous_flow) * pulse_amp * seg.get("amp", 1.0)
                previous_flow = flow
                phase += 1
                excitation = derivative + (rng.random() * 2.0 - 1.0) * breath * 0.08
            if seg["noise"] > 0 and kind != "closure":
                excitation += (rng.random() * 2.0 - 1.0) * seg["noise"]
            if seg["voiced"]:
                tilt_state = (1.0 - tilt) * excitation + tilt * tilt_state
                shaped = tilt_state
            else:
                shaped = excitation
            if kind in VOICED_KINDS and formants and seg.get("amp", 0) > 0:
                if step % 32 == 0:
                    bandwidth_scale = 1.0 + breath * 1.8
                    freqs = (
                        formants[0] * scale,
                        formants[1] * scale,
                        formants[2] * scale,
                        min(3500.0 * scale, SR * 0.40),
                        min(4600.0 * scale, SR * 0.46),
                    )
                    bands = (70 * bandwidth_scale, 100 * bandwidth_scale, 150 * bandwidth_scale, 230, 320)
                    for index in range(5):
                        configure(index, freqs[index], bands[index])
                value = shaped
                for index in range(5):
                    value = resonate(index, value * (0.35 if index else 1.0))
                radiated = value - 0.97 * previous_tract
                previous_tract = value
                sample = radiated
            elif seg["noise"] > 0:
                if step % 32 == 0:
                    configure(5, min(seg["nfreq"] * (0.9 + 0.1 * scale), SR * 0.46), seg["nbw"])
                sample = resonate(5, shaped)
            else:
                sample = resonate(0, 0.0) * 0.02
            output[cursor] = sample
            cursor += 1
        if seg.get("f"):
            previous_formants = seg["f"]

    mean = sum(output) / len(output)
    centered = [sample - mean for sample in output]
    peak = max(abs(sample) for sample in centered) or 1.0
    gained = [sample * (0.89 / peak) for sample in centered]
    polished = []
    previous = 0.0
    for sample in gained:
        bright = sample - previous
        previous = sample
        polished.append((1.0 - clarity * 0.25) * sample + clarity * 0.25 * bright)
    peak = max(abs(sample) for sample in polished) or 1.0
    if peak > 0.89:
        polished = [sample * (0.89 / peak) for sample in polished]
    return polished


def _clamp(value, low, high):
    return max(low, min(high, float(value)))


def preset_catalog():
    rows = []
    for presentation in PRESENTATIONS:
        for age in AGES:
            profile = dict(PRESETS[(presentation, age)])
            profile.update({"presentation": presentation, "age": age})
            rows.append(profile)
    return rows
