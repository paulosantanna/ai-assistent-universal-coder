# audio-engineering

Entry point: `audio-engineering-mcp/server.py`, skill `00_skills/(tooling)/voice-engineering-expert/SKILL.md`
Updated: 2026-11-03

- MCP `audio-engineering` is an active stdio JSON-RPC server (`2025-11-25`) owned by `codenavi-agent`. Tools: `audio.health`, `audio.search`, `audio.topic`, `audio.sources`, `audio.calculate`, `audio.voice_profile`, `audio.render_voice`.
- Corpus is original notes in `audio-engineering-mcp/corpus.py`, with public pointers consulted 2026-11-03: MIT OCW 6.003, RES.6-008, 6.341, MIT KEMAR, Stanford CCRMA, EBU R 128, ITU-R BS.1770, AES, Sound On Sound, Shure, ISO 3382-1, Praat, Klatt 1980/1990, Moore and Glasberg, Escudero et al. 2009, Barbosa 2008, Hillenbrand et al. 1995, W3C SSML, eSpeak NG, Opus. Standard text is not vendored.
- Super-skill `voice-engineering-expert` renders original pt-BR broadcast and General American voices (masculine/feminine × child/adult/older) to 22050 Hz 16-bit WAV plus JSON. No donor audio and no commercial voice API.
- Ceiling, verified by `scripts/self_check.py`: source-filter formant synthesis. Not a blind-test claim of human indistinguishability. eSpeak NG is cited for that public ceiling and is not imported.
- Accent target is a named reference (`pt-BR-broadcast`, `en-US-general-american`), not the absence of dialect.
- Safety: clone, impersonation, fraud and sexual use refuse before any file is written. Child presets require a non-empty use context.
- Catalog count moved from 305 to 306. Gate: `python quality/validate.py --runtime` PASS on 2026-11-03, including the protocol probe.
