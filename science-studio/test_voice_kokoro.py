"""Behavioral regression for pronunciation normalization across timing retries."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import voice_kokoro


class VoiceNormalizationTest(unittest.TestCase):
    def test_timing_retry_uses_same_normalized_text(self):
        project = {'scenes': [{'duration': 60, 'narration': 'texto original'}]}
        with tempfile.TemporaryDirectory() as folder, \
                patch.object(voice_kokoro, 'build_pipeline', return_value=(object(), 'cpu')), \
                patch.object(voice_kokoro, 'normalize_for_speech', return_value='texto normalizado'), \
                patch.object(voice_kokoro, 'synth', side_effect=[30.0, 60.0]) as synth, \
                patch.object(voice_kokoro, 'run'), \
                patch.object(voice_kokoro, 'probe', return_value={'format': {'duration': '60'}}):
            voice_kokoro.narrate(project, Path(folder), 'pm_alex', 1.0, 'cpu')
        self.assertEqual([call.args[1] for call in synth.call_args_list],
                         ['texto normalizado', 'texto normalizado'])


if __name__ == '__main__':
    unittest.main()
