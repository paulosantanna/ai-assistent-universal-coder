# Local transcription environment

Updated: 2026-10-13
Entry point: ../SKILL.md. Source: IMG_2756–IMG_2761; implementation: ../scripts/transcribe.py.

Use an actually approved Python environment with openai-whisper, PyTorch and NumPy, and a verified local MODEL.pt under --model-dir. Setup is a separate explicit dependency action: no bootstrap script or corporate mirror is assumed installed. Do not weaken certificate verification, add fake webrtcvad stubs or upload private media to recover a missing prerequisite.
The helper accepts --audio FILE or --audio-dir FOLDER; --list is engine-free and does not transcribe. A folder with multiple files requires --select all or comma-separated zero-based indexes. Colliding output stems are rejected; choose separate output directories.
CPU is default. --device cuda/auto is used only when the user requested acceleration; --model auto chooses small for CPU or an estimated available-memory fit for CUDA. Estimates are not measured performance guarantees. Only existing selected model files load; no network download. CUDA absence fails explicitly; OOM falls back only with --allow-cpu-fallback.
Mono PCM16 16kHz WAV is decoded directly. Other inputs need the actually installed Whisper/FFmpeg decoder; unsupported format blocks processing. Model file integrity/provenance must be verified before use.
Default language pt; --language auto enables engine detection, --initial-prompt seeds punctuation, --srt emits timestamped subtitles. Output includes cached UTF-8 TXT and JSON engine metadata; stdout uses VOX-AURUM BEGIN/END markers. Redirect stdout/stderr separately on Windows and read saved UTF-8 artifacts when console encoding differs.
Syntax: `python -X utf8 "00_skills/(tooling)/vox-aurum/scripts/transcribe.py" --audio "audio.wav" --model small --model-dir "LOCAL_MODELS" --out-dir "OUTPUT" --srt`. Interpreter is the verified target environment, not necessarily system Python.
Missing module → use/prepare the approved environment. Missing checkpoint → obtain verified weights through the authorized provider separately. No punctuation → inspect initial prompt/audio; keep literal recognized text, do not silently edit it. Nonzero exit → inspect failure and artifact completeness, never declare success merely because a file exists.
Official sources: [Whisper](https://github.com/openai/whisper), [local-checkpoint loader](https://github.com/openai/whisper/blob/main/whisper/__init__.py). Exact installed package compatibility is checked at use, not guaranteed by photo version numbers.
