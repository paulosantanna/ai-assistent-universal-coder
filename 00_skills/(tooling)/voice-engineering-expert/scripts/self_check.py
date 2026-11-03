#!/usr/bin/env python3
"""Behavioral checks for the parametric voice engine and the MCP handshake."""
import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MCP = ROOT / "audio-engineering-mcp"
sys.path.insert(0, str(MCP))

from corpus import SOURCES, TOPICS  # noqa: E402
from g2p import text_to_phones  # noqa: E402
from knowledge import calculate, search  # noqa: E402
from safety import VoiceRefusal  # noqa: E402
from synth import synthesize  # noqa: E402


def expect(condition, detail):
    if not condition:
        raise SystemExit("FAIL " + detail)


def main():
    source_ids = {item["id"] for item in SOURCES}
    for topic in TOPICS:
        missing = [item for item in topic["source_ids"] if item not in source_ids]
        expect(not missing, topic["id"] + " missing sources " + ",".join(missing))
    expect(len({item["org"] for item in SOURCES}) >= 12, "too few source organizations")

    phones = [phone for phone, _stress in text_to_phones("Olá, eu sou uma voz sintética.", "pt-BR")["phones"]]
    expect(phones[:3] == ["o", "l", "a"], "olá lost its lateral: " + " ".join(phones[:3]))
    expect("tsh" in phones, "broadcast ti affricate missing")
    english = [phone for phone, _stress in text_to_phones("Hello, this is a synthetic voice.", "en-US")["phones"]]
    expect("r" not in english and "h" in english and "v" in english, "english demo phones drifted")

    for presentation, age in (
        ("masculine", "adult"), ("feminine", "adult"),
        ("masculine", "child"), ("feminine", "child"),
        ("masculine", "older"), ("feminine", "older"),
    ):
        context = "narração educacional" if age == "child" else "teste de preset"
        rendered = synthesize(
            "a", language="pt-BR", presentation=presentation, age=age,
            phonemes="a a a a a a", intonation="flat", use_context=context,
        )
        metrics = rendered["measurements"]
        ratio = metrics["f0_hz"] / metrics["f0_target_hz"]
        expect(metrics["f0_hz"] is not None and 0.82 <= ratio <= 1.18, presentation + " " + age + " f0 " + str(metrics))
        expect(metrics["peak"] < 0.95 and metrics["rms"] > 0.05 and metrics["crest"] < 40, "level " + str(metrics))

    for text, language in (
        ("Olá, eu sou uma voz sintética.", "pt-BR"),
        ("Hello, this is a synthetic voice.", "en-US"),
    ):
        rendered = synthesize(text, language=language, presentation="feminine", age="adult", use_context="narração de aplicativo")
        metrics = rendered["measurements"]
        expect(metrics["duration_s"] > 0.4 and metrics["rms"] > 0.02 and metrics["peak"] < 0.95, language + " sentence " + str(metrics))
        expect(rendered["ceiling"].startswith("parametric-formant"), "ceiling missing")

    for kwargs in (
        dict(text="oi", language="pt-BR", presentation="feminine", age="adult", use_context="clonar a voz"),
        dict(text="oi", language="pt-BR", presentation="feminine", age="child", use_context=""),
        dict(text="oi", language="pt-BR", presentation="feminine", age="adult", use_context="ok", extra={"reference_audio": "donor.wav"}),
    ):
        try:
            synthesize(**kwargs)
        except VoiceRefusal:
            continue
        raise SystemExit("FAIL safety allowed a blocked render")

    expect(abs(calculate("nyquist", {"sample_rate": 48000})["value"] - 24000) < 1e-6, "nyquist")
    expect(calculate("erb", {"frequency_hz": 1000})["value"] > 100, "erb")
    expect(any(hit["id"] == "sampling-nyquist" for hit in search("MIT Nyquist")), "search MIT")
    expect(any(hit["id"] == "klatt-formant" for hit in search("Klatt")), "search Klatt")
    expect(any(hit["id"] == "loudness-lufs" for hit in search("EBU LUFS")), "search EBU")

    with tempfile.TemporaryDirectory() as directory:
        rendered = synthesize("a", language="pt-BR", presentation="masculine", age="adult", phonemes="a a a", use_context="teste", intonation="flat")
        from measure import write_wav
        wav_path = Path(directory) / "probe.wav"
        write_wav(wav_path, rendered["samples"], rendered["sample_rate"])
        with wave.open(str(wav_path), "rb") as handle:
            expect(handle.getnchannels() == 1 and handle.getframerate() == 22050 and handle.getsampwidth() == 2, "wav header")
            expect(handle.getnframes() == len(rendered["samples"]), "wav length")

    handshake(directory if False else None)
    print("PASS voice-engineering-expert self-check")
    return 0


def handshake(_unused):
    proc = subprocess.Popen(
        [sys.executable, "server.py"], cwd=MCP, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    def request(number, method, params):
        payload = json.dumps({"jsonrpc": "2.0", "id": number, "method": method, "params": params}) + "\n"
        proc.stdin.write(payload.encode())
        proc.stdin.flush()
        line = proc.stdout.readline()
        reply = json.loads(line)
        expect(reply.get("id") == number and "result" in reply, method + " failed")
        return reply["result"]
    try:
        init = request(1, "initialize", {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "self-check", "version": "1"}})
        expect(init["protocolVersion"] == "2025-11-25" and "tools" in init["capabilities"], "initialize")
        proc.stdin.write(b'{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}\n')
        proc.stdin.flush()
        listed = request(2, "tools/list", {})
        declared = json.loads((MCP / "tools.json").read_text(encoding="utf-8"))["tools"]
        expect(listed["tools"] == declared, "tools drifted from tools.json")
        request(3, "ping", {})
        with tempfile.TemporaryDirectory() as directory:
            called = request(4, "tools/call", {"name": "audio.render_voice", "arguments": {
                "text": "Olá.", "language": "pt-BR", "presentation": "feminine", "age": "adult",
                "out_dir": directory, "use_context": "narração de aplicativo", "intonation": "flat",
            }})
        expect(called["isError"] is False, "render tool failed")
    finally:
        proc.kill()
        proc.wait(timeout=5)


if __name__ == "__main__":
    sys.exit(main())
