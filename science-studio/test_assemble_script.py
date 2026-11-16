"""Behavioral checks for narration-length gates in the script assembler."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import assemble_script


class NarrationLengthGate(unittest.TestCase):
    def test_under_and_over_length_contract(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'script').mkdir()
            source = {'id': 'fixture', 'url': 'https://example.org/fixture',
                      'accessed': '2026-10-31', 'excerpt': 'Synthetic fixture.'}
            (root / 'sources.json').write_text(json.dumps({'sources': [source]}), encoding='utf-8')
            cases = [
                ('short', 'Este texto é muito curto.', [], 2),
                ('short_relaxed', 'Este texto é muito curto.', ['--allow-words-out-of-range'], 2),
                ('long', ' '.join(f'word{i}' for i in range(140)) + '.', [], 2),
                ('long_relaxed', ' '.join(f'word{i}' for i in range(140)) + '.',
                 ['--allow-words-out-of-range'], 0),
            ]
            for name, narration, flags, expected in cases:
                scene = {'narration': narration, 'visual': 'Fixture image', 'duration': 60,
                         'claims': ['fixture'], 'transition': 'cut', 'sd_prompt': 'fixture art'}
                fragment = {'chapter': 1, 'title': 'Fixture', 'scenes': [scene]}
                (root / 'script' / 'chapter-01.json').write_text(json.dumps(fragment), encoding='utf-8')
                out = root / f'{name}.json'
                with self.subTest(name=name), contextlib.redirect_stdout(io.StringIO()), \
                     contextlib.redirect_stderr(io.StringIO()):
                    actual = assemble_script.main([str(root), '--topic', 'fixture', '--profile',
                                                   'short', '--out', str(out), *flags])
                    self.assertEqual(actual, expected)
                    self.assertEqual(out.exists(), expected == 0)


if __name__ == '__main__':
    unittest.main()
