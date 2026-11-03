"""Deterministic acoustic helpers. Formulas are named; standards are not copied."""
import math
import struct
import wave


def nyquist(sample_rate):
    return float(sample_rate) / 2.0


def wavelength(frequency_hz, speed_m_s=343.0):
    if frequency_hz <= 0:
        raise ValueError("frequency_hz must be positive")
    return float(speed_m_s) / float(frequency_hz)


def sabine_rt60(volume_m3, absorption_sabins):
    if volume_m3 <= 0 or absorption_sabins <= 0:
        raise ValueError("volume and absorption must be positive")
    return 0.161 * float(volume_m3) / float(absorption_sabins)


def eyring_rt60(volume_m3, surface_m2, alpha):
    if not (0 < alpha < 1) or volume_m3 <= 0 or surface_m2 <= 0:
        raise ValueError("eyring inputs out of range")
    return 0.161 * float(volume_m3) / (-float(surface_m2) * math.log(1.0 - float(alpha)))


def erb(frequency_hz):
    """Moore and Glasberg ERB, frequency in hertz, result in hertz."""
    return 24.7 * (4.37 * (float(frequency_hz) / 1000.0) + 1.0)


def hz_from_cents(reference_hz, cents):
    return float(reference_hz) * (2.0 ** (float(cents) / 1200.0))


NOTE_OFFSETS = {
    "C": -9, "C#": -8, "DB": -8, "D": -7, "D#": -6, "EB": -6,
    "E": -5, "F": -4, "F#": -3, "GB": -3, "G": -2, "G#": -1, "AB": -1,
    "A": 0, "A#": 1, "BB": 1, "B": 2,
}


def hz_from_note(note):
    """Scientific pitch, A4 = 440 Hz. Accepts A3, C#4, Bb2."""
    text = note.strip().replace("♭", "b").replace("♯", "#")
    if len(text) < 2:
        raise ValueError("note must look like A4")
    octave = int(text[-1])
    name = text[:-1].upper().replace("B", "B")
    if name not in NOTE_OFFSETS and name.endswith("B") and len(name) == 2:
        name = name[0] + "B"
    if name not in NOTE_OFFSETS:
        raise ValueError("unknown note name")
    semitone = (octave - 4) * 12 + NOTE_OFFSETS[name]
    return 440.0 * (2.0 ** (semitone / 12.0))


def write_wav(path, samples, sample_rate):
    """16-bit mono PCM with one-LSB rectangular dither."""
    import random
    rng = random.Random(sample_rate + len(samples))
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        frames = bytearray()
        for sample in samples:
            dither = (rng.random() - rng.random()) / 32768.0
            value = max(-1.0, min(1.0, sample + dither))
            frames += struct.pack("<h", int(round(value * 32767.0)))
        handle.writeframes(frames)


def signal_metrics(samples, sample_rate):
    if not samples:
        return {"rms": 0.0, "peak": 0.0, "duration_s": 0.0, "crest": None, "f0_hz": None}
    peak = max(abs(sample) for sample in samples)
    mean_square = sum(sample * sample for sample in samples) / len(samples)
    rms = math.sqrt(mean_square)
    crest = (peak / rms) if rms > 1e-9 else None
    return {
        "sample_rate": sample_rate,
        "duration_s": len(samples) / float(sample_rate),
        "peak": peak,
        "rms": rms,
        "crest": crest,
        "f0_hz": estimate_f0(samples, sample_rate),
        "clipping": peak >= 0.999,
    }


def estimate_f0(samples, sample_rate, fmin=70.0, fmax=460.0):
    """Pick the most periodic window so consonants do not hide the voice."""
    count = len(samples)
    window = int(sample_rate * 0.28)
    if count < int(sample_rate * 0.12):
        return None
    if count <= window:
        f0, ratio = _f0_window(samples, sample_rate, fmin, fmax)
        return f0 if ratio >= 0.25 else None
    best_f0 = None
    best_ratio = 0.0
    step = max(window // 2, 1)
    for start in range(0, count - window + 1, step):
        f0, ratio = _f0_window(samples[start:start + window], sample_rate, fmin, fmax)
        if ratio > best_ratio:
            best_ratio = ratio
            best_f0 = f0
    return best_f0 if best_ratio >= 0.25 else None


def _f0_window(frame, sample_rate, fmin, fmax):
    mean = sum(frame) / len(frame)
    frame = [sample - mean for sample in frame]
    min_lag = max(1, int(sample_rate / fmax))
    max_lag = min(len(frame) // 2, int(sample_rate / fmin))
    if max_lag <= min_lag:
        return None, 0.0
    best = 0.0
    best_lag = min_lag
    step = 2 if len(frame) > 3000 else 1
    span = range(0, len(frame) - max_lag, step)
    if not span:
        return None, 0.0
    for lag in range(min_lag, max_lag):
        corr = 0.0
        for index in span:
            corr += frame[index] * frame[index + lag]
        if corr > best:
            best = corr
            best_lag = lag
    stepped = sum(frame[index] * frame[index] for index in span) or 1.0
    ratio = best / stepped if best > 0 else 0.0
    if ratio <= 0:
        return None, 0.0
    return sample_rate / float(best_lag), ratio
