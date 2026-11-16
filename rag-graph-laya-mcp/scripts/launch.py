"""Launch only this package's local runtimes; credentials stay in Windows Credential Manager."""
import json
import os
import secrets
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / '.state'


def occupied(port):
    with socket.socket() as sock:
        return sock.connect_ex(('127.0.0.1', port)) == 0


def main(*, existing=None):
    if os.name != 'nt':
        raise ValueError('Portable launcher is Windows-only; use the documented external Neo4j setup on Linux')
    existing = {} if existing is None else existing
    roles = {7687: 'neo4j_pid', 8008: 'model_pid', 8765: 'api_pid'}
    for port in roles:
        if occupied(port) and roles[port] not in existing:
            raise ValueError(f'Port {port} is occupied; do not interrupt an unrelated service')
    manifest = json.loads((STATE / 'runtime/manifest.json').read_text())['graph']
    java_home, neo4j_home = Path(manifest['java_home']), Path(manifest['neo4j_home'])
    import win32cred
    target = 'CodENavi/GraphRAG-Laya/Neo4j'
    try:
        stored = win32cred.CredRead(target, win32cred.CRED_TYPE_GENERIC)
        blob = stored['CredentialBlob']
        password = blob.decode('utf-16-le') if isinstance(blob, bytes) else blob
    except Exception as exc:
        if getattr(exc, 'winerror', None) != 1168:
            raise
        password = secrets.token_urlsafe(32)
        win32cred.CredWrite({'Type': win32cred.CRED_TYPE_GENERIC, 'TargetName': target,
                            'UserName': 'neo4j', 'CredentialBlob': password,
                            'Persist': win32cred.CRED_PERSIST_LOCAL_MACHINE}, 0)
    env = dict(os.environ, JAVA_HOME=str(java_home), NEO4J_HOME=str(neo4j_home),
               RGL_NEO4J_PASSWORD=password, HF_HUB_DISABLE_TELEMETRY='1', DO_NOT_TRACK='1',
               HF_HOME=str(STATE / 'models'), HF_HUB_DISABLE_PROGRESS_BARS='1', SEMAPHORE_LIMIT='1',
               ANONYMIZED_TELEMETRY='false')
    conf = neo4j_home / 'conf/neo4j.conf'
    conf.write_text('''server.default_listen_address=127.0.0.1
server.bolt.listen_address=127.0.0.1:7687
server.http.listen_address=127.0.0.1:7474
server.memory.heap.initial_size=512m
server.memory.heap.max_size=2g
server.memory.pagecache.size=512m
dbms.security.auth_enabled=true
dbms.usage_report.enabled=false
''', encoding='utf-8')
    java = str(java_home / 'bin/java.exe')
    common = [java, '-cp', str(neo4j_home / 'lib/*'), '-Dneo4j.home=' + str(neo4j_home)]
    if not (neo4j_home / 'data/dbms/auth.ini').exists() and not (neo4j_home / 'data/databases/system').exists():
        # Invoke Java directly; never expand runtime credentials in a shell command.
        initial = subprocess.run([*common, 'org.neo4j.cli.AdminTool', 'dbms', 'set-initial-password', password],
                                 cwd=neo4j_home, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 creationflags=subprocess.CREATE_NO_WINDOW)
        if initial.returncode:
            raise ValueError('Neo4j initial credential setup failed; no credential content is logged')
    processes = []
    def start(command, port):
        if roles[port] in existing:
            return existing[roles[port]]
        process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        processes.append(process)
        for _ in range(120):
            if process.poll() is not None:
                raise ValueError(f'Runtime for port {port} exited during startup')
            if occupied(port):
                return process.pid
            time.sleep(.5)
        raise ValueError(f'Runtime for port {port} did not become ready')
    try:
        graph_pid = start([*common, 'org.neo4j.server.startup.Neo4jBoot', 'console'], 7687)
        model_pid = start([sys.executable, str(ROOT / 'model_server.py')], 8008)
        api_pid = start([sys.executable, str(ROOT / 'server.py'), '--web'], 8765)
    except BaseException:
        for process in processes:
            if process.poll() is None:
                process.terminate()
        raise
    receipt = {'neo4j_pid': graph_pid, 'model_pid': model_pid, 'api_pid': api_pid,
               'panel': 'http://127.0.0.1:8765', 'credential_provider': target,
               'scope': 'This package only; passwords never enter files or stdout'}
    (STATE / 'launch.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
