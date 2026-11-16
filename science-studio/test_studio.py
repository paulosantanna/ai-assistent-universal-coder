"""Real FFmpeg fixture checks, not a generated science film or evaluated narrator."""
import copy
import json
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

import studio


def png(path, subject=False):
    w, h = 160, 284
    rows = []
    for y in range(h):
        row = bytearray()
        for x in range(w):
            if subject:
                row.extend((240, 20, 20, 255) if 40 < x < 65 and 100 < y < 145 else (0, 0, 0, 0))
            else:
                row.extend((10, 25 + x, 80 + y // 3, 255))
        rows.append(b'\x00' + row)
    def chunk(name, data):
        return struct.pack('!I', len(data)) + name + data + struct.pack('!I', zlib.crc32(name + data))
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('!2I5B', w, h, 8, 6, 0, 0, 0))
                     + chunk(b'IDAT', zlib.compress(b''.join(rows))) + chunk(b'IEND', b''))


class StudioContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='science-studio-')
        cls.root = Path(cls.temporary.name)
        png(cls.root / 'bg.png')
        png(cls.root / 'fg.png', subject=True)
        studio.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=frequency=220:duration=4',
                    '-ar', '48000', str(cls.root / 'voice.wav')])
        cls.project = {'version': '0.2', 'topic': 'Synthetic contract fixture; not science narration',
            'language': 'pt-BR', 'profile': 'short', 'duration': 4, 'size': [160, 284], 'fps': 12,
            'speech_balloons': False, 'sources': [{'id': 'fixture', 'url': 'https://ffmpeg.org/ffmpeg-filters.html',
            'accessed': '2026-10-27', 'excerpt': 'Synthetic audio/video test only, no scientific claim.'}],
            'scenes': [{'duration': 4, 'narration': 'Fixture audiovisual com duas camadas; áudio de teste, sem narrador.',
                        'visual': 'Synthetic red foreground over blue gradient, no artistic production claim.',
                        'claims': ['fixture'], 'audio': 'voice.wav', 'transition': 'fade',
                        'layers': [{'path': 'bg.png', 'scale': 1.08, 'x0': -4, 'x1': -8, 'zoom_end': 1.03},
                                   {'path': 'fg.png', 'x0': 0, 'x1': 30}]}]}
        studio.write(cls.root / 'project.json', cls.project)
        cls.result = studio.render(cls.project, cls.root)

    @classmethod
    def tearDownClass(cls):
        # The artifact is copied by the runner before cleanup when a durable smoke is needed.
        cls.temporary.cleanup()

    def test_real_streams_duration_and_layer_motion(self):
        result = studio.probe(self.root / 'preview.mp4')
        self.assertEqual({s['codec_type'] for s in result['streams']}, {'audio', 'video'})
        self.assertLess(abs(float(result['format']['duration']) - 4), 0.5)
        centers = []
        for timestamp in ('0.5', '3.5'):
            pixels = studio.run(['ffmpeg', '-v', 'error', '-ss', timestamp, '-i', str(self.root / 'preview.mp4'),
                                  '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
            locations = [i // 3 % 160 for i in range(0, len(pixels), 3)
                         if pixels[i] > 150 and pixels[i + 1] < 80 and pixels[i + 2] < 80]
            self.assertTrue(locations)
            centers.append(sum(locations) / len(locations))
        self.assertGreater(centers[1] - centers[0], 15)

    def test_cache_does_not_rerender_valid_scene(self):
        before = {p.name: p.stat().st_mtime_ns for p in (self.root / 'render').glob('*.mp4')}
        studio.render(self.project, self.root)
        after = {p.name: p.stat().st_mtime_ns for p in (self.root / 'render').glob('*.mp4')}
        self.assertEqual(before, after)

    def test_claims_duration_paths_and_audio_fail_closed(self):
        for change in ('claims', 'duration', 'path', 'audio'):
            bad = copy.deepcopy(self.project)
            if change == 'claims': bad['scenes'][0]['claims'] = ['invented']
            elif change == 'duration': bad['duration'] = 60
            elif change == 'path': bad['scenes'][0]['layers'][0]['path'] = '../outside.png'
            else: bad['scenes'][0]['duration'] = 10
            with self.assertRaises(ValueError): studio.validate(bad, self.root)

    def test_export_requires_review_and_stale_assets_invalidate_it(self):
        (self.root / 'approval.json').unlink(missing_ok=True)
        with self.assertRaises(OSError): studio.export(self.project, self.root)
        with self.assertRaises(ValueError): studio.review(self.project, self.root, 'fixture', ['science'])
        studio.review(self.project, self.root, 'fixture test only', ['science', 'visual', 'voice', 'subtitles', 'rights'])
        self.assertFalse(studio.export(self.project, self.root)['published'])
        altered = copy.deepcopy(self.project)
        altered['topic'] += ' modified'
        with self.assertRaises(ValueError): studio.export(altered, self.root)
        original = (self.root / 'subtitles.srt').read_bytes()
        (self.root / 'subtitles.srt').write_bytes(original + b'changed')
        try:
            with self.assertRaises(ValueError): studio.export(self.project, self.root)
        finally:
            (self.root / 'subtitles.srt').write_bytes(original)

    def test_opaque_single_layer_cannot_be_approved(self):
        bad = copy.deepcopy(self.project)
        bad['scenes'][0]['layers'] = bad['scenes'][0]['layers'][:1]
        with self.assertRaisesRegex(ValueError, 'separated_layers'):
            studio.review(bad, self.root, 'fixture', ['science', 'visual', 'voice', 'subtitles', 'rights'])

    def test_provider_errors_do_not_echo_provider_output(self):
        with self.assertRaises(ValueError) as error:
            studio.run([sys.executable, '-c', 'import sys; print("secret-fixture-value"); sys.exit(7)'])
        self.assertNotIn('secret-fixture-value', str(error.exception))

    def test_completed_provider_stages_resume(self):
        adapter = self.root / 'adapter.py'
        adapter.write_text('from pathlib import Path\np=Path("calls.txt")\np.write_text((p.read_text() if p.exists() else "")+"x")\n')
        config = self.root / 'providers.json'
        studio.write(config, {'providers': {s: [sys.executable, str(adapter)] for s in studio.STAGES}})
        studio.generate(self.root / 'project.json', config)
        studio.generate(self.root / 'project.json', config)
        self.assertEqual((self.root / 'calls.txt').read_text(), 'xxxx')

    def test_all_profiles_initialize_with_requested_defaults(self):
        for name, (duration, width, height) in studio.PROFILES.items():
            output = self.root / name
            result = subprocess.run([sys.executable, str(Path(studio.__file__)), 'init', '--topic', 'Cosmologia',
                                     '--profile', name, '--output', str(output)], capture_output=True)
            self.assertEqual(result.returncode, 0)
            project = studio.read(output / 'project.json')
            self.assertEqual((project['duration'], project['size']), (duration, [width, height]))
            self.assertEqual(project['voice'], 'male-documentary-deep')
            self.assertFalse(project['speech_balloons'])

    def test_custom_110_minute_duration_requires_matching_scenes(self):
        project = copy.deepcopy(self.project)
        project.update(profile='documentary', duration=6600)
        project['scenes'] = [dict(copy.deepcopy(self.project['scenes'][0]), duration=60)
                             for _ in range(110)]
        self.assertEqual(len(studio.validate(project, self.root, media=False)), 110)
        with self.assertRaisesRegex(ValueError, 'total_duration_mismatch'):
            studio.validate(dict(project, scenes=project['scenes'][:-1]), self.root, media=False)
        with self.assertRaises(ValueError):
            studio.validate(dict(project, duration=6601,
                scenes=project['scenes'] + [dict(project['scenes'][0], duration=1)]),
                self.root, media=False)


if __name__ == '__main__':
    unittest.main(verbosity=2)
