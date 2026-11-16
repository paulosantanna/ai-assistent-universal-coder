# Playbook — Science Studio AI v0.2

Updated: 2026-10-27. Entry point: [CLI](studio.py). Owner: codenavi-agent. Inherit AGENTS.md and CodENavi Full Workspace v2. Specialized steps are skills, never additional identities.

Objective: theme → evidence → script → layered cartoon art → documentary narration → animated MP4 → human review → local delivery. No automatic publication. Model/license/runtime failures block dependent stages and preserve prior outputs. Risk: medium for local artifacts; remote publication is separately governed.

## Profiles and entry points

| Profile | Target | Canvas | Editorial destination |
| --- | --- | --- | --- |
| short (default) | 60 s | 1080×1920 / 30 fps | TikTok, Shorts, Reels |
| youtube | 600 s | 1920×1080 / 30 fps | YouTube |
| documentary | 3600 s | 1920×1080 / 30 fps | Documentary |
| full-documentary | 5400 s | 1920×1080 / 30 fps | Full documentary |

These are requested editorial defaults, not claims about current platform maximums. Long profiles require many distinct researched scenes and storage/GPU/time planning. No 60/90-minute output is claimed until actually generated and inspected. Runtime accepts per-scene duration 1–60 s and validates total target; planning normally uses 10 s scenes.

## Six-phase execution

1. **BRIEFING:** read project notebook and [session contract](SESSION.md). Resolve theme and duration; defaults already define PT-BR, masculine deep documentary voice, no balloons, automatic preparation with human review. Check actual provider availability before promising automatic generation.
2. **RECON:** `python science-studio/studio.py doctor`. Check FFmpeg filter support, local Ollama model, ComfyUI API workflows/pesos, Piper model and voice sample/license. Do not install dependencies or use paid APIs silently. Research scientific sources via available tools or a local reviewed source corpus. Record sources and limitations.
3. **PLAN:** freeze outline/storyboard, claims, chapter arc and visual bible. Initialize project; prepare sources.json and local config. Seed project PROGRESS with the gates below. Distinguish artistic illustration from simulation. All profiles use the same JSON contract.
4. **EXECUTE:** research → script → assets → voice → scene render → concat. `generate` invokes configured local argv adapters; supplied assets may instead use `render`. Checkpoints/cache allow retry. Chapter-level editorial planning is required before long-form drafting; the built-in draft adapter offers bounded batches and previous-scene context, not a guaranteed coherent finished film.
5. **VERIFY:** inspect actual preview, claims, alpha/independent motion, voice, SRT and rights. Check A/V/duration/geometry. Human review of final full timeline is required; sample frames or an LLM self-check do not replace it. Record reviewer and all five checks only after explicit operator confirmation.
6. **DEBRIEF:** export reviewed local pack. Update quartet with verified state, blockers and next commands. Publication remains separate; revalidate target platform rules and existing publisher gates before any explicit publishing request.

## Step contracts and skills

| Step / skill | Inputs → outputs | Gate / failure action |
| --- | --- | --- |
| [Orchestrator](../00_skills/(tooling)/science-studio-expert/SKILL.md) | theme/profile/capabilities → project/checklist | No invented provider installation; keep project local |
| [Research](../00_skills/(tooling)/science-research-expert/SKILL.md) | scientific question/corpus → sources + claim ledger | Actual supported claims; block unsupported scene |
| [Script](../00_skills/(tooling)/science-script-expert/SKILL.md) | sources/outline → narrated scenes/visual/claims/timing | Source IDs and total duration valid; revise false certainty |
| [Layered art](../00_skills/(tooling)/motion-comic-art-expert/SKILL.md) | visual bible/scenes → local RGBA layers | Real alpha, continuity/overscan/rights; segment opaque assets |
| [Animation](../00_skills/(tooling)/motion-comic-animation-expert/SKILL.md) | layers/timing → independent motion/clips | Frames/duration/edges; rerender only invalid scenes |
| [Scientific VFX](../00_skills/(tooling)/science-vfx-expert/SKILL.md) | phenomenon/reference → controlled effect layers/clips | Honest illustration labels, no fake physical validation |
| [PT-BR voice](../00_skills/(tooling)/ptbr-documentary-voice-expert/SKILL.md) | narration/glossary/model → WAV per scene | Listen to real sample, timing/pitch/pronunciation; rewrite drift |
| [Review](../00_skills/(tooling)/science-video-review-expert/SKILL.md) | preview/project/rights → approval + delivery | science, visual, voice, subtitles, rights; missing check blocks export |

## CLI

Run from workspace root. No extra Python packages are needed by the compositor. FFmpeg/ffprobe must be installed. AI engines/models are separate prerequisites.

```powershell
python science-studio/studio.py doctor
python science-studio/studio.py init --topic "Como buracos negros deformam a luz" --profile short --output .work/meu-filme
```

For other durations replace profile with `youtube`, `documentary` or `full-documentary`. Use a new output directory for each production. The init command creates a real empty contract, not a fictional completed screenplay.

Configure installed engines once, with your real paths/model ID:

```powershell
python science-studio/studio.py configure --sources "C:/Science/sources.json" --ollama-model "SEU_MODELO_INSTALADO" --background-workflow "C:/Science/background-api.json" --foreground-workflow "C:/Science/foreground-api.json" --voice-engine kokoro --output .work/science-local.json
python science-studio/studio.py generate .work/meu-filme/project.json --config .work/science-local.json
```

Workflows are ComfyUI **API-format** graphs exported from an actually working local workflow, not browser UI graph JSON. Bind prompt string with `__PROMPT__`, seed integer with `__SEED__` placeholder; use a SaveImage output. Foreground workflow must actually segment/matte to RGBA; a text prompt requesting transparency is insufficient. Sources corpus must have been inspected; this adapter imports the ledger, it does not perform web search or certify claims.

## Voice engines

| Engine | Adapter | Credential | Use |
| --- | --- | --- | --- |
| Kokoro (default local) | `voice_kokoro.py` | none; local weights | PT-BR documentary narration, free/offline, voices `pm_alex`, `pm_santa`, `pf_dora` |
| Google Cloud TTS | `voice_google.py` | `GOOGLE_TTS_API_KEY` at runtime | genuine Google voices; fails closed without the key, never falls back silently |
| Piper (legacy) | `providers.py voice` | local `.onnx` | older projects that already bind the Piper model |

```powershell
python science-studio/studio.py configure --sources "C:/Science/sources.json" --ollama-model "SEU_MODELO_INSTALADO" --background-workflow "C:/Science/background-api.json" --foreground-workflow "C:/Science/foreground-api.json" --voice-engine kokoro --kokoro-python ".work/science-engines/kokoro-venv/Scripts/python.exe" --kokoro-voice pm_alex --output .work/science-local.json
python science-studio/studio.py configure ... --voice-engine google --google-voice pt-BR-Neural2-B --output .work/science-google.json
```

Kokoro fits every scene to its duration by changing the natural speech rate first and applying only a small residual atempo, so documentary cadence is preserved. Google voice names must be confirmed against the live account with `python science-studio/voice_google.py --list-voices`. API keys are runtime credentials: never stored in the project, config or notebook.

### Documentary mix (explicit delivery step)

The compositor renders narration only. The delivery mix is a separate, explicit step that treats the voice, adds a calm licensed-free music bed and ducks the music under the narration:

```powershell
python science-studio/audio_mix.py --input .work/meu-filme/preview.mp4 --in-place --record .work/meu-filme/render.json
```

`--in-place` replaces the reviewed preview with the mixed file and refreshes `render.json`, so the approved artifact and the exported file are the same bytes. `--music <file>` uses a supplied track instead of the procedural bed. Measured target: voice at -16 LUFS integrated, true peak -1.5 dBFS.

### Pipeline Gates (obrigatórios para dark-videos)

Após `render` e `audio_mix`, execute os 4 gates obrigatórios antes de `review`/`export`:

```powershell
python science-studio/studio.py gates .work/meu-filme/project.json
```

Gates verificados em sequência (falha em qualquer um bloqueia):

| Gate | Verificação | Critério de falha |
|---|---|---|
| 1. The-Fool Adversarial | Roteiro sem repetições, sem fragmentos | Palavra repetida >2x, fragmento curto (exceto abreviações) |
| 2. Asset Rights Audit | Assets sem gameplay/filme/série, sem rotação/espelhamento | Asset >60s, rotate≠0, gameplay detectado |
| 3. Music Select | Trilha calma licenciada-livre presente | Ausência de música |
| 4. Final Score ≥ 9.5 | Score técnico ≥ 9.5/10 | Narração, silêncios, música, rights, decode, review, duração |

Só prossiga para `review` e `export` se `gates` retornar `"gates": "pass"`.

### Delivery destination

Every dark-videos / Science Studio video is saved under `D:\Git\dark-videos` (workspace copy stays the source of truth; the delivery pack and the voice samples are copied there).

With externally authored assets/project (including images/clips generated through chat), use:

```powershell
python science-studio/studio.py validate .work/meu-filme/project.json
python science-studio/studio.py render .work/meu-filme/project.json
```

Open `review.html`, watch `preview.mp4`, inspect `subtitles.srt` and verify project sources/rights. Subtitles are sidecar SRT, estimated per words until aligned/reviewed. No burned-in subtitles or music mixer is claimed in the current compositor. Prepare a final burn-in or platform subtitle upload as an explicitly verified delivery step if required.

Only after the operator confirms the five review dimensions:

```powershell
python science-studio/studio.py review .work/meu-filme/project.json --reviewer "operador" --checks science visual voice subtitles rights
python science-studio/studio.py export .work/meu-filme/project.json
```

`delivery/final.mp4`, SRT, project, approval and handoff are reviewed local files. There is deliberately no publish command. Scientific verification and review are human/session work; structural gates protect traceability and file integrity.

## Dark-videos

The integration package in [integration](integration/) mounts an authenticated local API and a Science Studio page in the inspected Dark-videos checkout. It invokes this same CLI; it never puts generated videos into the mining/publishing queue. It requires local server configuration for workspace path, projects root and provider config. Missing config returns a concrete blocked state. Install through the reviewed installer with filesystem permission; activation/restart is separate from writing files. See [integration instructions](integration/INSTALL.md).

## Supported now versus authored extensions

Implemented: local composition, independent linear offsets, centered zoom per layer, RGBA images/video, blur, cut/fade, narration, SRT, per-scene cache, review/export and optional adapters for local sources/Ollama/ComfyUI plus the Kokoro, Google Cloud TTS and Piper voice engines. Scientific lensing, particle systems and advanced transitions are authored/generated effect layers or video clips, not implemented scientific solvers. Advanced rigging, forced alignment and automatic scientific truth verification are not implied. Music bed and voice ducking exist only in the separate `audio_mix.py` delivery step, not inside the compositor. Finish those assets with the skills and available engines before claiming the artistic goal is met.

## Evidence and recovery

`project.json` is source of truth; `stages.json` records provider checkpoints, `render/` caches scene MP4, `render.json` binds content/video/SRT hashes, `approval.json` binds the reviewed delivery. Never edit approval to bypass stale output. On missing media/provider, fix the actual prerequisite; don't substitute blank frames, silence or repeated clips. On source/asset change, validate and render again. Cache is project-local; archive completed projects without deleting originals automatically.
