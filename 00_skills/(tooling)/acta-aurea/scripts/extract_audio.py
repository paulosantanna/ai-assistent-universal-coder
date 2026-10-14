"""Extract 16 kHz mono WAV from authorized local media using an existing decoder."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import wave

def decoder(explicit):
    for candidate in (explicit, os.environ.get('ACTA_FFMPEG'), shutil.which('ffmpeg')):
        if candidate:
            path = Path(candidate)
            if not path.is_file():
                raise ValueError('Configured FFmpeg executable does not exist')
            return str(path.resolve())
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return None

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--meta-out', type=Path, required=True)
    parser.add_argument('--ffmpeg')
    args = parser.parse_args()
    temporary = None
    try:
        if not args.video.is_file():
            raise ValueError('Source media does not exist')
        if args.video.resolve() in (args.out.resolve(), args.meta_out.resolve()):
            raise ValueError('Output must not overwrite source media')
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(suffix='.wav', prefix='acta-extract-', dir=args.out.parent, delete=False) as staging:
            temporary = Path(staging.name)
        executable = decoder(args.ffmpeg)
        if executable:
            result = subprocess.run([executable, '-nostdin', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(args.video), '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', str(temporary)], capture_output=True, text=True)
            if result.returncode:
                raise ValueError('FFmpeg failed to decode source media; inspect format and decoder installation')
        else:
            import av
            with av.open(str(args.video)) as container, wave.open(str(temporary), 'wb') as output:
                output.setnchannels(1)
                output.setsampwidth(2)
                output.setframerate(16000)
                resampler = av.AudioResampler(format='s16', layout='mono', rate=16000)
                for frame in container.decode(audio=0):
                    for converted in resampler.resample(frame):
                        output.writeframes(converted.to_ndarray().tobytes())
                for converted in resampler.resample(None):
                    output.writeframes(converted.to_ndarray().tobytes())
        with wave.open(str(temporary), 'rb') as audio:
            duration = audio.getnframes() / audio.getframerate()
            if audio.getnchannels() != 1 or audio.getsampwidth() != 2 or audio.getframerate() != 16000 or duration <= 0:
                raise ValueError('Extracted WAV does not meet mono/16kHz/PCM16/nonempty contract')
        with args.video.open('rb') as source_file:
            source_hash = hashlib.file_digest(source_file, 'sha256').hexdigest()
        metadata = {'filename': args.video.name, 'source': str(args.video.resolve()), 'bytes': args.video.stat().st_size, 'sha256': source_hash, 'duration': duration, 'sample_rate': 16000, 'channels': 1}
        temporary.replace(args.out)
        args.meta_out.parent.mkdir(parents=True, exist_ok=True)
        args.meta_out.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print('Extraction complete: mono PCM16 WAV, metadata and source hash')
        return 0
    except (ValueError, OSError, ImportError, RuntimeError) as error:
        print('Extraction blocked: ' + str(error), file=sys.stderr)
        return 2
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()

if __name__ == '__main__':
    raise SystemExit(main())
