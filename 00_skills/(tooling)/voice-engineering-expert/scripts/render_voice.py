#!/usr/bin/env python3
"""Render one original parametric voice to WAV plus JSON."""
import argparse
import json
import sys
from pathlib import Path

MCP = Path(__file__).resolve().parents[4] / "audio-engineering-mcp"
sys.path.insert(0, str(MCP))

from measure import write_wav  # noqa: E402
from safety import VoiceRefusal  # noqa: E402
from synth import synthesize  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Render an original parametric voice.")
    parser.add_argument("--text", required=True)
    parser.add_argument("--language", required=True, choices=("pt-BR", "en-US"))
    parser.add_argument("--presentation", required=True, choices=("masculine", "feminine"))
    parser.add_argument("--age", required=True, choices=("child", "adult", "older"))
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--use-context", required=True)
    parser.add_argument("--intonation", default="auto")
    parser.add_argument("--tuning-cents", type=float, default=0)
    parser.add_argument("--f0-hz", type=float)
    parser.add_argument("--brightness", type=float)
    parser.add_argument("--breath", type=float)
    parser.add_argument("--formant-scale", type=float)
    parser.add_argument("--rate", type=float, default=1)
    parser.add_argument("--phonemes", default="")
    parser.add_argument("--no-affricate", action="store_true")
    args = parser.parse_args()
    try:
        rendered = synthesize(
            text=args.text,
            language=args.language,
            presentation=args.presentation,
            age=args.age,
            intonation=args.intonation,
            tuning_cents=args.tuning_cents,
            f0_hz=args.f0_hz,
            brightness=args.brightness,
            breath=args.breath,
            formant_scale=args.formant_scale,
            rate=args.rate,
            phonemes=args.phonemes or None,
            affricate_ti=not args.no_affricate,
            use_context=args.use_context,
        )
    except (VoiceRefusal, ValueError) as exc:
        print(json.dumps({"refused": True, "reason": str(exc)}, ensure_ascii=False))
        return 2
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = "voice-{}-{}-{}-{}".format(
        args.language.replace("-", "").lower(), args.presentation, args.age, rendered["seed"]
    )
    wav_path = out_dir / (stem + ".wav")
    manifest_path = out_dir / (stem + ".json")
    write_wav(wav_path, rendered["samples"], rendered["sample_rate"])
    manifest = {key: value for key, value in rendered.items() if key != "samples"}
    manifest["wav"] = str(wav_path)
    manifest["format"] = {"encoding": "PCM", "bit_depth": 16, "channels": 1}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"wav": str(wav_path), "manifest": str(manifest_path), "ceiling": manifest["ceiling"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
