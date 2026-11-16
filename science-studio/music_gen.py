"""Gerador de trilha calma/relaxante original para documentários (sem direitos autorais).

Composição procedural determinística: progressão harmônica em Lá menor,
pad quente, arpejo suave tipo sino e baixo discreto, com ambiência por delays.
Saída WAV 48 kHz estéreo. Nenhuma amostra externa; tudo sintetizado localmente.

Uso:
  python music_gen.py --minutes 8 --output calm.wav [--seed 42]
"""
from __future__ import annotations

import argparse
import math
import wave
from pathlib import Path

import numpy as np

SR = 48000


def note(freq, dur, amp, attack, decay, harmonics=(1.0, 0.5, 0.25, 0.12)):
    """Nota sintetizada com envelopes e harmônicos (timbre tipo sino/pad)."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    wave_out = np.zeros(n)
    for k, h in enumerate(harmonics, 1):
        # leve desafinação entre harmônicos para riqueza
        detune = 1.0 + 0.0004 * (k - 1)
        wave_out += h * np.sin(2 * math.pi * freq * detune * t)
    env = np.ones(n)
    a = max(1, int(attack * SR))
    d = max(1, int(decay * SR))
    env[:a] = np.linspace(0, 1, a) ** 2
    env[-d:] *= np.linspace(1, 0, d) ** 2
    return amp * wave_out * env


def pad_note(freq, dur, amp):
    return note(freq, dur, amp, attack=3.0, decay=3.0, harmonics=(1.0, 0.35, 0.12))


def bell_note(freq, amp):
    return note(freq, 3.2, amp, attack=0.01, decay=1.8, harmonics=(1.0, 0.55, 0.22, 0.08))


def compose(minutes: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    total = int(minutes * 60 * SR)
    out = np.zeros(total + 4 * SR)
    bpm = 66.0
    beat = 60.0 / bpm           # ~0.909 s
    bar = 4 * beat

    # Progressão em Lá menor: Am - F - C - G (frequências em Hz)
    A3, C4, E4 = 220.00, 261.63, 329.63
    F3, F4, A4 = 174.61, 349.23, 440.00
    C4b, E4b, G4 = 261.63, 329.63, 392.00
    G3, B3, D4 = 196.00, 246.94, 293.66
    G2, F2, C3, A2 = 98.00, 87.31, 130.81, 110.00

    chords = [
        # (root bass, [notas do pad], [arpejo])
        (A2, [A3, C4, E4], [A3, C4, E4, C4]),
        (F2, [F3, A3 * 0.5, F4], [F4, A4, F4 * 0.5, A4]),
        (C3, [C4b, G4, E4b], [E4b, G4, C4b * 1.0, G4]),
        (G2, [G3, B3, D4], [D4, B3, G3 * 1.0, B3]),
    ]

    def place(signal, at):
        i = int(at * SR)
        j = min(len(out), i + len(signal))
        if i < len(out):
            out[i:j] += signal[: j - i]

    t = 0.0
    bar_index = 0
    while t < minutes * 60:
        bass_f, pad_notes, arp_notes = chords[bar_index % 4]
        # pad: acorde inteiro, sustentado por 2 compassos
        for f in pad_notes:
            place(pad_note(f, bar * 2.2, 0.16), t)
        # baixo suave
        place(pad_note(bass_f, bar * 1.9, 0.20), t)
        # arpejo: notas a cada meio-tempo
        for k, f in enumerate(arp_notes * 2):
            at = t + k * (bar / 8)
            place(bell_note(f, 0.11 + 0.03 * rng.random()), at)
        t += bar * 2
        bar_index += 1

    # ambiência: delays simples em L/R (sem convolução pesada)
    def add_delay(sig, taps, stereo_lag):
        result = np.copy(sig)
        for lag, gain in taps:
            s = int(lag * SR)
            shifted = np.zeros_like(sig)
            shifted[s:] = sig[:-s]
            result += gain * shifted
        left = result
        lag = int(stereo_lag * SR)
        right = np.copy(result)
        right[lag:] = right[:-lag]
        right[:lag] = 0
        # pequena diferença de fase para alargar
        return np.stack([left, right], axis=1)

    stereo = add_delay(out, [(0.37, 0.30), (0.62, 0.18), (0.95, 0.10)], 0.011)

    # fades
    a = int(6 * SR)
    stereo[:a] *= np.linspace(0, 1, a)[:, None]
    e = int(8 * SR)
    stereo[-e:] *= np.linspace(1, 0, e)[:, None]

    # normalização para pico -1.5 dBFS
    peak = np.abs(stereo).max()
    if peak > 0:
        stereo = stereo / peak * 10 ** (-1.5 / 20)
    return stereo


def write_wav(path: Path, data: np.ndarray):
    samples = (np.clip(data, -1.0, 1.0) * 32767).astype('<i2')
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(samples.tobytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--minutes', type=float, default=8.0)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    if not 1.0 <= args.minutes <= 90.0:
        raise ValueError('minutes_out_of_range')
    data = compose(args.minutes, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_wav(args.output, data)
    print(f'music_done: {args.output} ({args.minutes} min, 48 kHz stereo)')


if __name__ == '__main__':
    main()
