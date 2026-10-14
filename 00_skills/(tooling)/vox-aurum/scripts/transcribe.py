"""Offline audio transcription; never downloads a model or installs an engine."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import wave

EXTENSIONS = {'.wav', '.mp3', '.m4a', '.ogg', '.flac', '.aac', '.wma'}
INITIAL_PROMPT = 'Olá, vamos começar. Esta é uma transcrição em português: com acentos, vírgulas, pontos e perguntas. O que foi discutido?'

def stamp(seconds, comma=True):
    ms = round(float(seconds) * 1000)
    return f'{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02}{"," if comma else "."}{ms % 1000:03}'

def select_files(args):
    if args.audio:
        if not args.audio.is_file():
            raise ValueError('Audio file does not exist')
        files = [args.audio.resolve()]
    elif args.audio_dir and args.audio_dir.is_dir():
        files = sorted(p.resolve() for p in args.audio_dir.iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS)
    else:
        raise ValueError('Provide an existing --audio or --audio-dir')
    if not files:
        raise ValueError('No supported audio files found')
    if args.list:
        return files
    if args.audio_dir:
        if args.select == 'all':
            selected = files
        elif args.select:
            indexes = [int(value) for value in args.select.split(',')]
            if len(set(indexes)) != len(indexes) or any(i < 0 or i >= len(files) for i in indexes):
                raise ValueError('Selection indexes must be unique and within the listed files')
            selected = [files[i] for i in indexes]
        elif len(files) == 1:
            selected = files
        else:
            raise ValueError('Multiple files: use --list then --select INDEXES or all')
    else:
        selected = files
    if len({p.stem for p in selected}) != len(selected):
        raise ValueError('Selected files have colliding output names; process them into separate destinations')
    return selected

def choose_model(requested, device, torch):
    if requested != 'auto':
        return requested
    if device == 'cpu':
        return 'small'
    available = torch.cuda.mem_get_info()[0] * .85 / (1024 ** 3)
    for model, gb in [('large-v3', 10), ('medium', 5), ('small', 2), ('base', 1), ('tiny', .5)]:
        if available >= gb:
            return model
    raise ValueError('Insufficient available GPU memory even for tiny; choose CPU explicitly')

def load_audio(path, whisper, np):
    if path.suffix.lower() == '.wav':
        with wave.open(str(path), 'rb') as audio:
            if audio.getnchannels() == 1 and audio.getsampwidth() == 2 and audio.getframerate() == 16000:
                return np.frombuffer(audio.readframes(audio.getnframes()), dtype='<i2').astype(np.float32) / 32768
    return whisper.load_audio(str(path))

def write_outputs(path, result, args, model, device):
    segments = result.get('segments', [])
    previous = 0.0
    for segment in segments:
        start, end = float(segment['start']), float(segment['end'])
        if start < previous or end <= start:
            raise ValueError('Engine produced invalid or unordered timestamps')
        previous = start
    args.out_dir.mkdir(parents=True, exist_ok=True)
    text = result['text'].strip()
    if not text:
        raise ValueError('No recognized text; inspect silence/audio quality')
    output = args.out_dir / (path.stem + '.txt')
    output.write_text(text + '\n', encoding='utf-8')
    if args.srt:
        subtitles = '\n\n'.join(f'{i}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"].strip()}' for i, s in enumerate(segments, 1))
        (args.out_dir / (path.stem + '.srt')).write_text(subtitles + '\n', encoding='utf-8')
    with path.open('rb') as source_file:
        source_hash = hashlib.file_digest(source_file, 'sha256').hexdigest()
    metadata = {'source': str(path), 'sha256': source_hash, 'language': result.get('language'), 'model': model, 'device': device, 'segments': segments}
    (args.out_dir / (path.stem + '.json')).write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if args.save_dir:
        args.save_dir.mkdir(parents=True, exist_ok=True)
        destination = args.save_dir / output.name
        if destination.exists() and destination.read_bytes() != output.read_bytes():
            raise ValueError('Save destination already contains different text; preserve it and choose another destination')
        destination.write_bytes(output.read_bytes())
    print(f'[VOX-AURUM:BEGIN:{path.name}]\n{text}\n[VOX-AURUM:END:{path.name}]')
    return output

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--audio', type=Path)
    group.add_argument('--audio-dir', type=Path)
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--select')
    parser.add_argument('--model', default='medium')
    parser.add_argument('--model-dir', type=Path, default=Path('models'))
    parser.add_argument('--out-dir', type=Path, default=Path('out'))
    parser.add_argument('--save-dir', type=Path)
    parser.add_argument('--language', default='pt')
    parser.add_argument('--device', choices=['cpu', 'cuda', 'auto'], default='cpu')
    parser.add_argument('--allow-cpu-fallback', action='store_true')
    parser.add_argument('--initial-prompt', default=INITIAL_PROMPT)
    parser.add_argument('--srt', action='store_true')
    args = parser.parse_args()
    try:
        files = select_files(args)
        if args.list:
            for i, path in enumerate(files):
                print(f'[{i}] {path.name}' + (' [decoder prerequisite]' if path.suffix.lower() != '.wav' else ''))
            return 0
        if args.model != 'auto' and not (args.model_dir / (args.model + '.pt')).is_file():
            raise ValueError('Local model checkpoint is missing; no download attempted')
        import torch
        import whisper
        import numpy as np
        device = args.device
        if device == 'auto':
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
        if device == 'cuda' and not torch.cuda.is_available():
            raise ValueError('CUDA unavailable; use the approved GPU runtime or request CPU explicitly')
        model_name = choose_model(args.model, device, torch)
        checkpoint = (args.model_dir / (model_name + '.pt')).resolve()
        if not checkpoint.is_file():
            raise ValueError('Selected local checkpoint is missing; no download attempted')
        model = whisper.load_model(str(checkpoint), device=device)
        for path in files:
            audio = load_audio(path, whisper, np)
            options = {'language': None if args.language == 'auto' else args.language, 'task': 'transcribe', 'fp16': device == 'cuda', 'initial_prompt': args.initial_prompt, 'verbose': False}
            try:
                result = model.transcribe(audio, **options)
            except torch.cuda.OutOfMemoryError:
                if not args.allow_cpu_fallback:
                    raise ValueError('CUDA out of memory; choose a smaller local model or authorize --allow-cpu-fallback') from None
                print('[vox-aurum] CUDA exhausted; explicit CPU fallback', file=sys.stderr)
                del model
                torch.cuda.empty_cache()
                device = 'cpu'
                model = whisper.load_model(str(checkpoint), device='cpu')
                options['fp16'] = False
                result = model.transcribe(audio, **options)
            write_outputs(path, result, args, model_name, device)
        return 0
    except (ValueError, OSError, ImportError, RuntimeError) as error:
        print('Transcription blocked: ' + str(error), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
