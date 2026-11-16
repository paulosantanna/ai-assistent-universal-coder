"""Separate local process: long renders never run inside HTTP requests."""
import json
import subprocess
import sys
from pathlib import Path

home, folder, action = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(home))
from studio import write

try:
    if action not in {'generate', 'render', 'review', 'export'}:
        raise ValueError('unsupported_action')
    write(folder / 'job.json', {'status': 'running', 'action': action})
    result = subprocess.run([sys.executable, str(home / 'studio.py'), action,
                             str(folder / 'project.json'), *sys.argv[4:]], capture_output=True)
    try:
        detail = json.loads(result.stdout.decode('utf-8').strip().splitlines()[-1])
    except (ValueError, IndexError):
        detail = {'error': 'worker_failed_inspect_local_prerequisites'}
    write(folder / 'job.json', {'status': 'done' if result.returncode == 0 else 'blocked',
                               'action': action, 'result': detail})
except (OSError, ValueError) as exc:
    write(folder / 'job.json', {'status': 'blocked', 'action': action, 'error': str(exc)})
finally:
    (folder / '.job.lock').unlink(missing_ok=True)
