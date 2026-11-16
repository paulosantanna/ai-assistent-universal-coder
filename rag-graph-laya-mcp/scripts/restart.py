"""Restart only this package's API or model process after verifying its recorded identity."""
import argparse
import json
import os
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

import psutil

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / '.state'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', action='store_true')
    args = parser.parse_args()
    with sqlite3.connect(STATE / 'ledger.sqlite3') as db:
        if db.execute("SELECT count(*) FROM jobs WHERE status IN('queued','running')").fetchone()[0]:
            raise ValueError('Active jobs exist; finish or cancel them before restarting the service')
    receipt = json.loads((STATE / 'launch.json').read_text())
    role = 'model_pid' if args.model else 'api_pid'
    process = psutil.Process(receipt[role])
    expected = str(ROOT / ('model_server.py' if args.model else 'server.py')).lower()
    descendants = process.children(recursive=True)
    if not any(expected in ' '.join(p.cmdline()).lower() for p in [process, *descendants]):
        raise ValueError('Recorded process no longer belongs to this runtime; refuse to stop it')
    for child in reversed(descendants):
        child.terminate()
    process.terminate()
    psutil.wait_procs([process, *descendants], timeout=10)
    import win32cred
    record = win32cred.CredRead('CodENavi/GraphRAG-Laya/Neo4j', win32cred.CRED_TYPE_GENERIC)
    blob = record['CredentialBlob']
    password = blob.decode('utf-16-le') if isinstance(blob, bytes) else blob
    env = dict(os.environ, RGL_NEO4J_PASSWORD=password, HF_HOME=str(STATE / 'models'),
               HF_HUB_DISABLE_TELEMETRY='1', DO_NOT_TRACK='1', HF_HUB_DISABLE_PROGRESS_BARS='1',
               SEMAPHORE_LIMIT='1', ANONYMIZED_TELEMETRY='false')
    command = [sys.executable, str(ROOT / 'model_server.py')] if args.model else [sys.executable, str(ROOT / 'server.py'), '--web']
    child = subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
    time.sleep(2)
    if child.poll() is not None:
        raise ValueError('Restarted process failed to remain active')
    receipt[role] = child.pid
    (STATE / 'launch.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    print(json.dumps({'restarted': role, 'pid': child.pid}))


if __name__ == '__main__':
    main()
