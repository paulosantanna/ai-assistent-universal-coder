"""Documentary audio mix: narration treatment, calm music bed and voice ducking.

The compositor renders narration only. This step produces the delivery mix:
EQ + compression + loudness normalisation for the voice, a calm licensed-free music
bed (procedural by default, or a supplied file), and sidechain ducking so the music
never competes with the narration. Video stream is copied untouched.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from studio import digest, probe, read, run, write  # noqa: E402

VOICE_CHAIN = (
    'highpass=f=85,lowpass=f=10000,'
    'equalizer=f=110:t=h:w=90:g=3,'
    'equalizer=f=3000:t=h:w=250:g=2.5,'
    'equalizer=f=6000:t=h:w=150:g=1.5,'
    'acompressor=threshold=0.06:ratio=3.5:attack=8:release=120:makeup=2'
)
MUSIC_TONES = ((110.0, 0.42), (164.81, 0.28), (220.0, 0.18), (261.63, 0.09), (329.63, 0.05))


def music_bed(duration, target, music_db):
    gain = 10 ** (music_db / 20)
    argv = ['ffmpeg', '-v', 'error', '-y']
    for frequency, _ in MUSIC_TONES:
        argv += ['-f', 'lavfi', '-i', f'sine=frequency={frequency}:sample_rate=48000:duration={duration}']
    labels = ''.join(f'[{index}:a]' for index in range(len(MUSIC_TONES)))
    weights = ' '.join(str(amplitude) for _, amplitude in MUSIC_TONES)
    filters = (f'{labels}amix=inputs={len(MUSIC_TONES)}:normalize=0:weights={weights}[pad];'
               '[pad]lowpass=f=700,aecho=0.8:0.9:45|90:0.22|0.12,'
               'tremolo=f=0.12:d=0.25,'
               f'afade=t=in:st=0:d=4,afade=t=out:st={max(0, duration - 4):.2f}:d=4,'
               f'volume={gain:.4f}[music]')
    argv += ['-filter_complex', filters, '-map', '[music]', '-ac', '1', '-ar', '48000', str(target)]
    run(argv)


def mix(source, output, music_file, music_db, lufs, duration, in_place=False):
    folder = output.parent
    folder.mkdir(parents=True, exist_ok=True)
    narration = folder / '.mix-narration.wav'
    music = folder / '.mix-music.wav'
    measured = probe(source)
    total = duration or float(measured['format']['duration'])
    run(['ffmpeg', '-v', 'error', '-y', '-i', str(source), '-vn',
         '-acodec', 'pcm_s16le', '-ar', '48000', '-ac', '1', str(narration)])
    if music_file:
        run(['ffmpeg', '-v', 'error', '-y', '-stream_loop', '-1', '-i', str(music_file), '-t', f'{total:.3f}',
             '-af', f'afade=t=in:st=0:d=3,afade=t=out:st={max(0, total - 3):.2f}:d=3,volume={10 ** (music_db / 20):.4f}',
             '-ac', '1', '-ar', '48000', str(music)])
    else:
        music_bed(total, music, music_db)
    filters = (f'[0:a]{VOICE_CHAIN},loudnorm=I={lufs}:TP=-1.5:LRA=11,asplit=2[voz_main][voz_key];'
               '[1:a][voz_key]sidechaincompress=threshold=0.04:ratio=8:attack=25:release=400:makeup=1[duck];'
               '[voz_main][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0:weights=1 0.9[out]')
    target = output
    temporary = folder / (output.stem + '.mixing.mp4')
    if in_place:
        target = temporary
    run(['ffmpeg', '-v', 'error', '-y', '-i', str(source), '-i', str(music),
         '-filter_complex', filters, '-map', '0:v:0', '-map', '[out]',
         '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2',
         '-t', f'{total:.3f}', '-movflags', '+faststart', str(target)])
    if in_place:
        os.replace(temporary, source)
        target = source
    narration.unlink(missing_ok=True)
    music.unlink(missing_ok=True)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--in-place', action='store_true')
    parser.add_argument('--record', type=Path,
                        help='render.json to refresh with the mixed video hash and duration')
    parser.add_argument('--music', type=Path)
    parser.add_argument('--music-db', type=float, default=-21.0)
    parser.add_argument('--lufs', type=float, default=-16.0)
    parser.add_argument('--duration', type=float)
    args = parser.parse_args()
    if not args.input.is_file():
        raise ValueError('input_missing')
    if args.music and not args.music.is_file():
        raise ValueError('music_missing')
    if not args.in_place and not args.output:
        raise ValueError('output_required_or_in_place')
    if args.in_place and args.output:
        raise ValueError('output_and_in_place_are_exclusive')
    if not -40.0 <= args.music_db <= 0.0:
        raise ValueError('music_db_out_of_range')
    if not -30.0 <= args.lufs <= -8.0:
        raise ValueError('lufs_out_of_range')
    source = args.input.resolve()
    output = (args.output or args.input).resolve()
    result = mix(source, output, args.music, args.music_db, args.lufs, args.duration, args.in_place)
    evidence = {'source': str(source), 'output': str(result),
                'output_sha256': digest(result), 'music': str(args.music) if args.music else 'procedural',
                'music_db': args.music_db, 'voice_lufs': args.lufs,
                'ducking': 'sidechaincompress threshold=0.04 ratio=8',
                'duration': float(probe(result)['format']['duration'])}
    write(result.parent / f'{result.stem}.audio-mix.json', evidence)
    if args.record:
        record = read(args.record)
        record['video_sha256'] = digest(result)
        record['duration'] = evidence['duration']
        record['audio_mix'] = evidence
        write(args.record, record)
    print(f'audio_mix_done: {result}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
