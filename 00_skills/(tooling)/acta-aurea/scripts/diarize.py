"""Offline anonymous diarization; labels are not speaker identities."""
import argparse
import json
from pathlib import Path
import re
import sys
import wave

def seconds(value):
    h, m, tail = value.replace(',', '.').split(':')
    return int(h) * 3600 + int(m) * 60 + float(tail)

def read_srt(path):
    result = []
    for block in re.split(r'\n\s*\n', path.read_text(encoding='utf-8-sig').strip()):
        lines = block.splitlines()
        timing = next((i for i, line in enumerate(lines) if ' --> ' in line), None)
        if timing is None:
            raise ValueError('Invalid SRT block')
        start, end = lines[timing].split(' --> ')
        start, end = seconds(start), seconds(end)
        if start < 0 or end <= start or (result and start < result[-1]['start']):
            raise ValueError('Invalid/unordered SRT timestamps')
        result.append({'start': start, 'end': end, 'text': '\n'.join(lines[timing + 1:]), 'speaker': None, 'offtopic': False})
    if not result:
        raise ValueError('Empty SRT')
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wav', type=Path, required=True)
    parser.add_argument('--srt', type=Path, required=True)
    parser.add_argument('--meta', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--num-speakers', type=int)
    parser.add_argument('--engine', choices=['resemblyzer', 'mfcc'], default='resemblyzer')
    args = parser.parse_args()
    try:
        segments = read_srt(args.srt)
        meta = json.loads(args.meta.read_text(encoding='utf-8'))
        if args.num_speakers is not None and args.num_speakers < 1:
            raise ValueError('Speaker count must be positive')
        import numpy as np
        from sklearn.cluster import AgglomerativeClustering
        from sklearn.metrics import silhouette_score
        with wave.open(str(args.wav), 'rb') as source:
            if source.getnchannels() != 1 or source.getsampwidth() != 2 or source.getframerate() != 16000:
                raise ValueError('Diarization requires mono 16kHz PCM16 WAV')
            audio = np.frombuffer(source.readframes(source.getnframes()), dtype='<i2').astype(np.float32) / 32768
        duration = len(audio) / 16000
        if any(s['end'] > duration + .1 for s in segments):
            raise ValueError('Subtitle timestamps exceed WAV duration')
        if args.engine == 'resemblyzer':
            from resemblyzer import VoiceEncoder
            encoder = VoiceEncoder(device='cpu', verbose=False)
            feature = encoder.embed_utterance
        else:
            import librosa
            def feature(part):
                mfcc = librosa.feature.mfcc(y=part, sr=16000, n_mfcc=20)
                return np.concatenate((mfcc.mean(axis=1), mfcc.std(axis=1)))
        windows = []
        # Merge contiguous subtitle speech into >=4s anchors before clustering.
        for segment in segments:
            if windows and segment['start'] - windows[-1][1] <= .5 and segment['end'] - windows[-1][0] <= 8:
                windows[-1][1] = max(windows[-1][1], segment['end'])
            else:
                windows.append([segment['start'], segment['end']])
        anchors = [window for window in windows if window[1] - window[0] >= 4]
        if len(anchors) < 2 and args.num_speakers != 1:
            raise ValueError('Too few long speech anchors; cannot produce trustworthy multi-speaker diarization')
        threshold = max(.005, float(np.sqrt(np.mean(audio ** 2))) * .2)
        def embedding(start, end):
            part = audio[int(start * 16000):int(end * 16000)]
            frames = [part[i:i + 480] for i in range(0, len(part), 480)]
            voiced = [frame for frame in frames if len(frame) and np.sqrt(np.mean(frame ** 2)) > threshold]
            if not voiced:
                raise ValueError('No voiced frames in a subtitle region; inspect transcript/audio alignment')
            vector = feature(np.concatenate(voiced))
            norm = np.linalg.norm(vector)
            if not norm or not np.all(np.isfinite(vector)):
                raise ValueError('Invalid speaker embedding')
            return vector / norm
        if args.num_speakers == 1:
            labels = [0] * len(segments)
            quality = None
        else:
            vectors = np.stack([embedding(*anchor) for anchor in anchors])
            counts = [args.num_speakers] if args.num_speakers else range(2, min(6, len(anchors) - 1) + 1)
            candidates = []
            for count in counts:
                if count < 2 or count >= len(anchors):
                    continue
                clustered = AgglomerativeClustering(n_clusters=count, metric='cosine', linkage='average').fit_predict(vectors)
                score = float(silhouette_score(vectors, clustered, metric='cosine'))
                candidates.append((score, clustered, count))
            if not candidates:
                raise ValueError('Insufficient anchors for the requested speaker count/quality check')
            quality, clustered, count = max(candidates, key=lambda item: item[0])
            centroids = np.stack([vectors[clustered == i].mean(axis=0) for i in range(count)])
            centroids /= np.linalg.norm(centroids, axis=1, keepdims=True)
            labels = [int(np.argmax(centroids @ embedding(s['start'], s['end']))) for s in segments]
        speakers = {}
        for segment, label in zip(segments, labels):
            key = 'S' + str(label + 1)
            segment['speaker'] = key
            speakers.setdefault(key, {'name': key, 'confirmed': False})
        times = {key: sum(s['end'] - s['start'] for s in segments if s['speaker'] == key) for key in speakers}
        call = {'media': meta, 'speakers': speakers, 'segments': segments, 'topics': [], 'meeting': {'participants': [], 'resumo_md': '', 'ata_md': '', 'acoes': [], 'glossario': []}, 'diarization': {'engine': args.engine, 'silhouette': quality, 'speech_seconds': times, 'warning': 'Anonymous estimates; confirm names and inspect overlap/quality before delivery'}}
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(call, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print('ACTA-AUREA:DIAR quality=' + str(quality) + ' speech_seconds=' + json.dumps(times))
        return 0
    except (ValueError, OSError, ImportError, RuntimeError, KeyError) as error:
        print('Diarization blocked: ' + str(error), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
