"""Bounded read-only MCP/LSP handshake probes, without inherited runtime secrets."""
import json
import os
import queue
import subprocess
import threading
import time


def environment():
    return {k: v for k, v in os.environ.items() if k.upper() in {'PATH', 'SYSTEMROOT', 'TEMP', 'TMP', 'TMPDIR', 'HOME'}}


def probe(command, cwd, kind, timeout=10):
    proc = subprocess.Popen(command, cwd=cwd, env=environment(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    inbox = queue.Queue()
    deadline = time.monotonic()+timeout

    def reader():
        try:
            while True:
                if kind == 'mcp':
                    data = proc.stdout.readline(1_000_001)
                else:
                    length = None
                    while True:
                        line = proc.stdout.readline(4096)
                        if not line:
                            raise EOFError()
                        if line == b'\r\n':
                            break
                        if line.lower().startswith(b'content-length:'):
                            length = int(line.split(b':', 1)[1])
                    if length is None or not 0 <= length <= 1_000_000:
                        raise ValueError('Invalid framing')
                    data = proc.stdout.read(length)
                if not data or len(data) > 1_000_000:
                    raise EOFError()
                inbox.put(json.loads(data))
        except (OSError, EOFError, ValueError):
            inbox.put(None)

    thread = threading.Thread(target=reader, daemon=True)
    thread.start()

    def send(message):
        data = json.dumps(message).encode('utf-8')
        if kind == 'mcp':
            data += b'\n'
        else:
            data = f'Content-Length: {len(data)}\r\n\r\n'.encode()+data
        proc.stdin.write(data)
        proc.stdin.flush()

    def request(number, method, params):
        send({'jsonrpc': '2.0', 'id': number, 'method': method, 'params': params})
        # Notifications cannot consume the deadline indefinitely.
        for _ in range(20):
            reply = inbox.get(timeout=max(0,deadline-time.monotonic()))
            if reply is None:
                raise ValueError('Protocol stream ended')
            if reply.get('id') == number:
                if reply.get('jsonrpc') != '2.0' or 'error' in reply or 'result' not in reply:
                    raise ValueError('Invalid RPC response')
                return reply['result']
        raise ValueError('Excess notifications')

    try:
        params = ({'protocolVersion': '2025-11-25', 'capabilities': {}, 'clientInfo': {'name': 'codenavi-quality', 'version': '1.0.0'}} if kind == 'mcp'
                  else {'processId': None, 'rootUri': None, 'capabilities': {}})
        result = request(1, 'initialize', params)
        if not isinstance(result, dict) or not isinstance(result.get('capabilities'), dict):
            raise ValueError('Missing initialization capabilities')
        send({'jsonrpc': '2.0', 'method': 'notifications/initialized' if kind == 'mcp' else 'initialized', 'params': {}})
        if kind == 'mcp':
            if result.get('protocolVersion') != '2025-11-25' or not isinstance(result.get('serverInfo'), dict) or 'tools' not in result['capabilities']:
                raise ValueError('MCP negotiation failed')
            tools = request(2, 'tools/list', {})
            if tools.get('nextCursor'):
                raise ValueError('Inventory must declare all paginated tools')
            request(3, 'ping', {})
            return {'passed': True, 'tools': tools['tools']}
        if request(2, 'shutdown', {}) is not None:
            raise ValueError('LSP shutdown must return null')
        send({'jsonrpc': '2.0', 'method': 'exit', 'params': {}})
        proc.wait(timeout=timeout)
        return {'passed': proc.returncode == 0}
    except (KeyError, TypeError, ValueError, OSError, queue.Empty, subprocess.TimeoutExpired):
        return {'passed': False}
    finally:
        if proc.poll() is None:
            proc.kill()
        proc.wait(timeout=5)
        proc.stdin.close()
        proc.stdout.close()
        thread.join(timeout=1)


probe.environment = environment
