"""Google Cloud Text-to-Speech adapter for genuine Google documentary voices.

The API key is a runtime credential: it is read from GOOGLE_TTS_API_KEY and is never
written to disk, logs or project files. Without the key the adapter fails closed,
because a silent fallback would hide which engine produced the narration.

Same audio contract as providers.py:voice:
  audio/{index:04}-raw.wav, audio/{index:04}.wav, scene['audio'] in project.json
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import struct
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from studio import probe, read, run, write  # noqa: E402
from ptbr_pronunciation import normalize_for_speech  # noqa: E402

ENDPOINT = 'https://texttospeech.googleapis.com/v1'
MAX_INPUT_BYTES = 4500
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


def api_key():
    key = os.environ.get('GOOGLE_TTS_API_KEY', '').strip()
    if not key:
        raise ValueError('google_tts_api_key_missing: set GOOGLE_TTS_API_KEY at runtime')
    return key


def call(route, payload=None):
    url = f'{ENDPOINT}{route}?key={api_key()}'
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(url, data=data,
                                     headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors='replace')[:400]
        raise ValueError(f'google_tts_http_error: {exc.code} {detail}') from None


def list_voices(language='pt-BR'):
    voices = call('/voices').get('voices', [])
    return [v for v in voices if v.get('languageCode') == language]


def wav_header(data_length, sample_rate=24000, channels=1, bits=16):
    byte_rate = sample_rate * channels * bits // 8
    block = channels * bits // 8
    return (b'RIFF' + struct.pack('<I', 36 + data_length) + b'WAVE'
            + b'fmt ' + struct.pack('<IHHIIHH', 16, 1, channels, sample_rate, byte_rate, block, bits)
            + b'data' + struct.pack('<I', data_length))


def split_text(text):
    chunks, current = [], ''
    for sentence in text.replace('\n', ' ').split('. '):
        piece = (sentence.rstrip('.') + '. ') if sentence.strip() else ''
        if len((current + piece).encode()) > MAX_INPUT_BYTES and current:
            chunks.append(current.strip())
            current = piece
        else:
            current += piece
    if current.strip():
        chunks.append(current.strip())
    return chunks or [text]


def synthesize(text, voice_name, language, speaking_rate, target):
    audio = bytearray()
    for chunk in split_text(text):
        payload = {'input': {'text': chunk},
                   'voice': {'languageCode': language, 'name': voice_name},
                   'audioConfig': {'audioEncoding': 'LINEAR16', 'sampleRateHertz': 24000,
                                   'speakingRate': speaking_rate, 'pitch': 0.0,
                                   'volumeGainDb': 0.0}}
        response = call('/text:synthesize', payload)
        if 'audioContent' not in response:
            raise ValueError('google_tts_missing_audio_content')
        audio += base64.b64decode(response['audioContent'])
    target.write_bytes(wav_header(len(audio)) + bytes(audio))
    return float(probe(target)['format']['duration'])


def narrate(project, root, voice_name, language, base_rate):
    if language != 'pt-BR':
        raise ValueError(f'google_tts_only_ptbr: language={language}; somente pt-BR é permitido')
    available = {v['name'] for v in list_voices(language)}
    if not available:
        raise ValueError(f'google_tts_no_voice_for_language: {language}')
    if voice_name not in available:
        raise ValueError(f'google_tts_voice_unavailable: {voice_name}; '
                         f'available={sorted(available)[:12]}')
    folder = root / 'audio'
    folder.mkdir(exist_ok=True)
    report = []
    for index, scene in enumerate(project['scenes']):
        duration = float(scene['duration'])
        raw = folder / f'{index:04}-raw.wav'
        target = folder / f'{index:04}.wav'
        rate = base_rate
        texto = normalize_for_speech(scene['narration'], language=language)
        actual = synthesize(texto, voice_name, language, rate, raw)
        for _ in range(3):
            tempo = actual / duration
            if 0.92 <= tempo <= 1.08:
                break
            candidate = min(max(rate * tempo, SPEED_RANGE[0]), SPEED_RANGE[1])
            if abs(candidate - rate) < 0.01:
                break
            rate = candidate
            actual = synthesize(scene['narration'], voice_name, language, rate, raw)
        residual = min(max(actual / duration, RESIDUAL_RANGE[0]), RESIDUAL_RANGE[1])
        run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af',
             f'atempo={residual:.4f},{NARRATION_CHAIN},apad',
             '-t', f'{duration:.3f}', '-ar', '48000', '-ac', '1', str(target)])
        final = float(probe(target)['format']['duration'])
        if abs(final - duration) > 0.3:
            raise ValueError(f'google_tts_timing_out_of_range_scene_{index}')
        scene['audio'] = target.relative_to(root).as_posix()
        report.append({'scene': index, 'voice': voice_name, 'speaking_rate': round(rate, 3),
                       'residual_atempo': round(residual, 3),
                       'engine_duration': round(actual, 3), 'target_duration': duration,
                       'final_duration': round(final, 3), 'ratio': round(final / duration, 3)})
    write(folder / 'google-tts-report.json',
          {'engine': 'google-cloud-tts', 'voice': voice_name, 'language': language, 'scenes': report})
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path)
    parser.add_argument('--voice', default='pt-BR-Neural2-B')
    parser.add_argument('--language', default='pt-BR')
    parser.add_argument('--rate', type=float, default=1.0)
    parser.add_argument('--list-voices', action='store_true')
    args = parser.parse_args()
    if args.list_voices:
        for voice in list_voices(args.language):
            print(f"{voice['name']}\t{voice.get('ssmlGender', '?')}\t{voice.get('naturalSampleRateHertz', '?')}")
        return 0
    if not args.project:
        raise ValueError('project_required')
    if not SPEED_RANGE[0] <= args.rate <= SPEED_RANGE[1]:
        raise ValueError('rate_out_of_range')
    file = args.project.resolve()
    project = read(file)
    narrate(project, file.parent, args.voice, args.language, args.rate)
    write(file, project)
    print(f'google_tts_voice_done: voice={args.voice} scenes={len(project["scenes"])}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
