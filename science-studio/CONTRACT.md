# Project and provider contract

Updated: 2026-10-27. Entry point: [playbook](PLAYBOOK.md).

`project.json` version 0.2 contains topic, profile, duration seconds, even-pixel size [width,height], fps, language=pt-BR, voice=male-documentary-deep, speech_balloons=false, sources and scenes. Defaults are created by init. Profiles are editorial targets; fixture projects may use reduced dimensions/duration for verification and must be identified as fixtures.

An explicitly authored total duration may be 1–6600 seconds (up to 110 minutes); scene durations must still be 1–60 seconds and sum to that total. The four profile defaults are unchanged.

Minimal authored scene (source excerpt must be supported by an actually inspected source):

```json
{
  "duration": 10,
  "narration": "A gravidade pode desviar a trajetória da luz. Nesta ilustração, vemos o fundo celeste deformado ao redor do objeto.",
  "visual": "Buraco negro ilustrativo, fundo estelar e nuvem em acreção, HQ detalhada sem balões",
  "claims": ["source-1"],
  "transition": "fade",
  "audio": "audio/0000.wav",
  "layers": [
    {"path": "assets/background.png", "kind": "image", "scale": 1.08, "zoom_end": 1.04, "x0": -20, "x1": -30, "y0": -20, "y1": -25},
    {"path": "assets/foreground.png", "kind": "image", "scale": 1.0, "zoom_end": 1.02, "x0": 0, "x1": 15, "y0": 0, "y1": -10}
  ]
}
```

Each source needs id, url, accessed date and excerpt (short quotation within rights limits, or clearly attributed factual paraphrase). Add detailed claim ledger and licenses when authoring; structural presence is not scientific correctness. Scene claims link source IDs; review checks each actual statement.

Layer position uses canvas pixels, scale is relative to canvas and zoom_end relative to layer starting scale. Layers are ordered back to front. x/y interpolate linearly during the scene; centered zoompan applies per layer. Overscan is explicit through scale/negative offsets. Images are stretched to the specified layer canvas; author crops/reframes to matching aspect beforehand. Video layers require at least scene duration, are never silently looped. Overlay effects can be RGBA images or supported alpha video codecs. blur is 0–20 pixels. Only cut/fade transitions are supported directly. Keep advanced effects inside pre-rendered clips.

Audio must have a real audio stream and duration within 350 ms of the scene. Final assembled duration must be within 500 ms. Rendering normalizes pixel format/codecs, not truth or artistic quality. Piper adapter applies single-pass loudnorm as an initial mix; measure final loudness if a precise mix target is required. SRT timing is estimated by words, not forced alignment. Discreet two-line layout/safe area and burn-in are editorial delivery tasks until implemented.

Providers config has `providers` mapping for research, script, assets and voice. Each value is an argv string array. `{project}` and `{root}` are substituted literally; shell execution is disabled. Configuration is trusted operator code, never accepted from an uploaded project or model response. Adapters modify only their project/assets and fail nonzero on problems; errors are not copied into ordinary logs because external engines may echo secrets.

- research imports reviewed local source JSON. Online research is performed by the session/tools before invoking this adapter.
- script uses Ollama local `/api/chat`, JSON mode and bounded 120-second batches. Validate global outline/coherence separately for long films.
- assets uses ComfyUI local `/prompt`, `/history/{id}`, `/view`; independent foreground graph must output real alpha. Background and foreground sharing prompt/seed does not guarantee geometry; visual review remains required.
- voice uses installed Piper CLI and a licensed local voice; language/timbre are evaluated by listening. No exact commercial/public-person imitation is assumed.

Pre-authenticated local provider URLs only. No raw runtime credentials in config/project. No paid providers used by default. No model weights, packages or voices installed by these scripts.

`generate` checkpoints completed stages if project and configuration remain unchanged. Operator edits invalidate the provider-stage checkpoint; prefer `render` for deliberately hand-edited projects to preserve custom assets. Per-scene render cache hashes content/assets/parameters/FFmpeg version. Input changes require rerender; review/export compare source, media and SRT hashes. File integrity is not a tamper-proof signature or a proof that the operator watched the video.
