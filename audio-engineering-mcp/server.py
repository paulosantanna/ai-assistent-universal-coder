#!/usr/bin/env python3
"""stdio JSON-RPC MCP for audio engineering and parametric voice rendering."""
import json
import sys
from pathlib import Path

from knowledge import calculate, health, search, sources, topic
from measure import write_wav
from phones import PRESETS
from safety import VoiceRefusal
from synth import CEILING, synthesize

ROOT = Path(__file__).resolve().parent
TOOLS = json.loads((ROOT / "tools.json").read_text(encoding="utf-8"))["tools"]
PROTOCOL = "2025-11-25"


def emit(payload):
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def ok(message_id, result):
    emit({"jsonrpc": "2.0", "id": message_id, "result": result})


def fail(message_id, code, message):
    emit({"jsonrpc": "2.0", "id": message_id, "error": {"code": code, "message": message}})


def safe_out_dir(value):
    raw = Path(value)
    if not value or ".." in raw.parts:
        raise ValueError("out_dir is unsafe")
    path = raw.resolve()
    cwd = Path.cwd().resolve()
    temporary = Path("/tmp").resolve()
    if path != cwd and cwd not in path.parents and path != temporary and temporary not in path.parents:
        raise ValueError("out_dir must stay under the working directory or /tmp")
    path.mkdir(parents=True, exist_ok=True)
    return path


def render_voice(arguments):
    out_dir = safe_out_dir(arguments["out_dir"])
    rendered = synthesize(
        text=arguments["text"],
        language=arguments["language"],
        presentation=arguments["presentation"],
        age=arguments["age"],
        intonation=arguments.get("intonation") or "auto",
        tuning_cents=arguments.get("tuning_cents") or 0,
        phonemes=arguments.get("phonemes") or None,
        use_context=arguments["use_context"],
    )
    stem = "voice-{language}-{presentation}-{age}-{seed}".format(
        language=arguments["language"].replace("-", "").lower(),
        presentation=arguments["presentation"],
        age=arguments["age"],
        seed=rendered["seed"],
    )
    wav_path = out_dir / (stem + ".wav")
    manifest_path = out_dir / (stem + ".json")
    write_wav(wav_path, rendered["samples"], rendered["sample_rate"])
    manifest = {key: value for key, value in rendered.items() if key != "samples"}
    manifest["wav"] = str(wav_path)
    manifest["format"] = {"encoding": "PCM", "bit_depth": 16, "channels": 1}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest["manifest"] = str(manifest_path)
    return manifest


def voice_profile(arguments):
    key = (arguments["presentation"], arguments["age"])
    if key not in PRESETS:
        raise ValueError("unknown voice preset")
    if arguments["language"] not in ("pt-BR", "en-US"):
        raise ValueError("language must be pt-BR or en-US")
    profile = dict(PRESETS[key])
    profile.update({
        "presentation": arguments["presentation"],
        "age": arguments["age"],
        "language": arguments["language"],
        "accent_target": "pt-BR-broadcast" if arguments["language"] == "pt-BR" else "en-US-general-american",
        "ceiling": CEILING,
        "child_profile_rule": "Narration preset only. Rendering still requires a non-empty non-sexual use_context.",
    })
    return profile


def call_tool(name, arguments):
    arguments = arguments or {}
    if name == "audio.health":
        return health()
    if name == "audio.search":
        return {"hits": search(arguments["query"], arguments.get("limit", 8))}
    if name == "audio.topic":
        return topic(arguments["id"])
    if name == "audio.sources":
        return sources(arguments.get("org"))
    if name == "audio.calculate":
        return calculate(arguments["operation"], arguments.get("arguments") or {})
    if name == "audio.voice_profile":
        return voice_profile(arguments)
    if name == "audio.render_voice":
        return render_voice(arguments)
    raise KeyError(name)


def handle(request):
    method = request.get("method")
    message_id = request.get("id")
    params = request.get("params") or {}
    if message_id is None:
        return
    if method == "initialize":
        ok(message_id, {
            "protocolVersion": PROTOCOL,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "audio-engineering", "version": "1.0.0"},
        })
        return
    if method == "tools/list":
        ok(message_id, {"tools": TOOLS})
        return
    if method == "ping":
        ok(message_id, {})
        return
    if method == "tools/call":
        try:
            result = call_tool(params.get("name"), params.get("arguments") or {})
            ok(message_id, {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}], "isError": False})
        except (VoiceRefusal, ValueError, KeyError, OSError) as exc:
            ok(message_id, {"content": [{"type": "text", "text": json.dumps({"refused": True, "reason": str(exc)}, ensure_ascii=False)}], "isError": True})
        return
    fail(message_id, -32601, "Method not found")


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            fail(None, -32700, "Parse error")
            continue
        try:
            handle(request)
        except Exception as exc:  # noqa: BLE001 — stdio server must answer instead of dying
            message_id = request.get("id") if isinstance(request, dict) else None
            if message_id is not None:
                fail(message_id, -32603, type(exc).__name__)


if __name__ == "__main__":
    main()
