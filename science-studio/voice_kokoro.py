"""Local PT-BR documentary narration with Kokoro (offline, free, Apache-2.0 weights).

Requires the isolated kokoro virtualenv (kokoro, misaki, espeak-ng, torch). It keeps
the audio contract of providers.py:voice:

  audio/{index:04}-raw.wav   engine output (24 kHz)
  audio/{index:04}.wav       48 kHz narration retimed to the scene duration
  scene['audio']             updated in project.json

Timing is fitted by changing the natural speech rate first and by applying only a
small residual atempo, so the documentary delivery keeps a natural cadence.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from studio import probe, read, run, write  # noqa: E402
from ptbr_pronunciation import normalize_for_speech  # noqa: E402

VOICES = ('pm_alex', 'pm_santa', 'pf_dora')
SPEED_RANGE = (0.85, 1.15)
RESIDUAL_RANGE = (0.90, 1.10)
NARRATION_CHAIN = (
    'highpass=f=85,lowpass=f=10000,'
    'equalizer=f=110:t=h:w=90:g=3,'
    'equalizer=f=3000:t=h:w=250:g=2.5,'
    'equalizer=f=6000:t=h:w=150:g=1.5,'
    'acompressor=threshold=0.06:ratio=3.5:attack=8:release=120:makeup=2,'
    'loudnorm=I=-16:TP=-1.5:LRA=11'
)


def build_pipeline(device):
    import espeakng_loader
    from phonemizer.backend.espeak.wrapper import EspeakWrapper
    from kokoro import KPipeline

    EspeakWrapper.set_library(espeakng_loader.get_library_path())
    os.environ['ESPEAK_DATA_PATH'] = espeakng_loader.get_data_path()
    if device == 'auto':
        import torch
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    return KPipeline(lang_code='p', repo_id='hexgrad/Kokoro-82M', device=device), device


def synth(pipeline, text, voice, speed, target):
    import numpy as np
    import soundfile as sf

    pieces = [audio.numpy() for _, _, audio in pipeline(text, voice=voice, speed=speed)]
    if not pieces:
        raise ValueError('kokoro_empty_audio')
    sf.write(target, np.concatenate(pieces), 24000)
    return float(probe(target)['format']['duration'])


def narrate(project, root, voice, base_speed, device):
    language = str(project.get('language', 'pt-BR'))
    if language != 'pt-BR':
        raise ValueError(f'kokoro_only_ptbr: language={language}; somente pt-BR é permitido')
    folder = root / 'audio'
    folder.mkdir(exist_ok=True)
    pipeline, device = build_pipeline(device)
    report = []
    for index, scene in enumerate(project['scenes']):
        duration = float(scene['duration'])
        raw = folder / f'{index:04}-raw.wav'
        target = folder / f'{index:04}.wav'
        speed = base_speed
        texto = normalize_for_speech(scene['narration'], language=language)
        actual = synth(pipeline, texto, voice, speed, raw)
        for _ in range(3):
            tempo = actual / duration
            if 0.92 <= tempo <= 1.08:
                break
            candidate = min(max(speed * tempo, SPEED_RANGE[0]), SPEED_RANGE[1])
            if abs(candidate - speed) < 0.01:
                break
            speed = candidate
            actual = synth(pipeline, texto, voice, speed, raw)
        residual = min(max(actual / duration, RESIDUAL_RANGE[0]), RESIDUAL_RANGE[1])
        run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af',
             f'atempo={residual:.4f},{NARRATION_CHAIN},apad',
             '-t', f'{duration:.3f}', '-ar', '48000', '-ac', '1', str(target)])
        final = float(probe(target)['format']['duration'])
        if abs(final - duration) > 0.3:
            raise ValueError(f'kokoro_timing_out_of_range_scene_{index}: ratio={final / duration:.2f}')
        scene['audio'] = target.relative_to(root).as_posix()
        report.append({'scene': index, 'voice': voice, 'speed': round(speed, 3),
                       'residual_atempo': round(residual, 3),
                       'engine_duration': round(actual, 3), 'target_duration': duration,
                       'final_duration': round(final, 3), 'ratio': round(final / duration, 3)})
    write(folder / 'kokoro-report.json',
          {'engine': 'kokoro-82M', 'device': device, 'voice': voice,
           'base_speed': base_speed, 'scenes': report})
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--voice', choices=VOICES, default='pm_alex')
    parser.add_argument('--speed', type=float, default=1.0)
    parser.add_argument('--device', choices=('auto', 'cpu', 'cuda'), default='auto')
    args = parser.parse_args()
    if not SPEED_RANGE[0] <= args.speed <= SPEED_RANGE[1]:
        raise ValueError('speed_out_of_range')
    file = args.project.resolve()
    project = read(file)
    narrate(project, file.parent, args.voice, args.speed, args.device)
    write(file, project)
    print(f'kokoro_voice_done: voice={args.voice} scenes={len(project["scenes"])}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
