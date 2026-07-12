from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest


def send_json(pipe, msg):
    payload = json.dumps(msg)
    pipe.write(f"Content-Length: {len(payload)}\r\n\r\n{payload}".encode("utf-8"))
    pipe.flush()


def _read_with_timeout(pipe, n, result):
    try:
        data = pipe.read(n)
        result.append(data)
    except Exception as e:
        result.append(e)


def _readline_with_timeout(pipe, result):
    try:
        line = pipe.readline()
        result.append(line)
    except Exception as e:
        result.append(e)


def recv_json(pipe, timeout=10.0):
    start = time.monotonic()
    headers = {}
    remaining = timeout
    while remaining > 0:
        result: list = []
        t = threading.Thread(target=_readline_with_timeout, args=(pipe, result))
        t.daemon = True
        t.start()
        t.join(remaining)
        if not result:
            return None  # timeout, no response
        if isinstance(result[0], Exception):
            raise result[0]  # type: ignore
        line: bytes = result[0]
        if not line:
            time.sleep(0.01)
            remaining = timeout - (time.monotonic() - start)
            continue
        line = line.decode("utf-8", errors="replace").strip()
        if not line:
            break  # empty line = end of headers
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()
        remaining = timeout - (time.monotonic() - start)
    length = int(headers.get("content-length", 0))
    if length == 0:
        return None
    remaining = timeout - (time.monotonic() - start)
    if remaining <= 0:
        return None
    result = []
    t = threading.Thread(target=_read_with_timeout, args=(pipe, length, result))
    t.daemon = True
    t.start()
    t.join(remaining)
    if not result:
        return None
    if isinstance(result[0], Exception):
        raise result[0]
    return json.loads(result[0].decode("utf-8"))


def init_and_open_doc(proc, uri, text, version=1):
    send_json(proc.stdin, {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"processId": os.getpid(), "rootUri": None, "capabilities": {}},
    })
    recv_json(proc.stdout, timeout=10)
    send_json(proc.stdin, {
        "jsonrpc": "2.0", "method": "initialized", "params": None,
    })
    send_json(proc.stdin, {
        "jsonrpc": "2.0", "method": "textDocument/didOpen",
        "params": {
            "textDocument": {"uri": uri, "languageId": "aeos", "version": version, "text": text},
        },
    })


@pytest.fixture
def lsp_server():
    proc = subprocess.Popen(
        [sys.executable, "-m", "aeos_lsp", "--stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(Path(__file__).resolve().parent.parent),
    )
    yield proc
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
