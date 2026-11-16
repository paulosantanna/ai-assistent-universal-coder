"""Idempotent Windows startup for the existing shared local RAG services.

Scope: installed runtimes only, no downloads/training or unrelated process stops.
Inputs: package-local runtime manifest and runtime Credential Manager reference.
Output: all three listeners owned by this package and authenticated health ready.
Failure: missing installation, foreign listener, startup timeout or unhealthy provider.
"""

import json
import os
import time
from contextlib import contextmanager
from pathlib import Path

import httpx
import launch
import psutil

ROOT = Path(__file__).resolve().parents[1]
PORTS = {7687: 'neo4j_pid', 8008: 'model_pid', 8765: 'api_pid'}


@contextmanager
def startup_lock():
    import msvcrt

    path = ROOT / '.state/startup.lock'
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as lock:
        lock.write(b'0')
        lock.flush()
        deadline = time.monotonic() + 30
        while True:
            lock.seek(0)
            try:
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise RuntimeError('RAG startup is busy; retry after the current start finishes') from None
                time.sleep(.25)
        try:
            yield
        finally:
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)


def owned_listeners():
    """Check actual listening process commands; stale receipt PIDs are not authority."""
    found = {}
    for connection in psutil.net_connections(kind='tcp'):
        if connection.status != psutil.CONN_LISTEN or connection.laddr.port not in PORTS:
            continue
        port = connection.laddr.port
        if connection.laddr.ip != '127.0.0.1' or not connection.pid:
            raise RuntimeError(f'Port {port} is not a package-owned loopback listener')
        process = psutil.Process(connection.pid)
        command = [str(arg).replace('\\', '/').lower() for arg in process.cmdline()]
        expected = str(ROOT / ('model_server.py' if port == 8008 else 'server.py')).replace('\\', '/').lower()
        if port == 7687:
            manifest = json.loads((ROOT / '.state/runtime/manifest.json').read_text())['graph']
            home = str(Path(manifest['neo4j_home'])).replace('\\', '/').lower()
            valid = (('org.neo4j.server.startup.neo4jboot' in command
                      and f'-dneo4j.home={home}' in command)
                     or ('org.neo4j.server.communityentrypoint' in command
                         and f'--home-dir={home}' in command))
        else:
            valid = expected in command
        if not valid:
            raise RuntimeError(f'Port {port} belongs to another service; it was not stopped')
        found[PORTS[port]] = connection.pid
    return found


def ready():
    try:
        with httpx.Client(timeout=10, trust_env=False, follow_redirects=False) as client:
            response = client.post('http://127.0.0.1:8765/api/tools/health', json={})
            response.raise_for_status()
            health = response.json()
        return (health.get('server') == 'rag-graph-laya'
                and health.get('model', {}).get('available') is True
                and health.get('model', {}).get('models', {}).get('paused') is False
                and health.get('neo4j', {}).get('available') is True)
    except (httpx.HTTPError, ValueError, AttributeError):
        return False


def main():
    if os.name != 'nt':
        raise RuntimeError('Automatic RAG startup requires the installed Windows runtime')
    with startup_lock():
        existing = owned_listeners()
        if len(existing) != len(PORTS):
            launch.main(existing=existing)
        deadline = time.monotonic() + 30
        while not ready():
            if time.monotonic() >= deadline:
                raise RuntimeError('RAG providers are not ready; inspect model and Neo4j health')
            time.sleep(.5)
        if len(owned_listeners()) != len(PORTS):
            raise RuntimeError('RAG listener disappeared during startup')
    print(json.dumps({'ready': True, 'server': 'rag-graph-laya'}))


if __name__ == '__main__':
    main()
