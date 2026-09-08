# Skill: aura-voice

## Mission
Ingest authorized audio/video/transcript sources, transcribe speech, preserve multilingual technical nomenclature, separate humor from serious statements, and produce evidence-backed conversation analysis without treating jokes, sarcasm or playful speech as factual commitments.

## Tool
- MCP: `aura-voice`
- Actions:
  - `aura.health`
  - `aura.media.inspect`
  - `aura.media.extract_audio`
  - `aura.transcript.read`
  - `aura.transcribe.local`
  - `aura.analyze.transcript`
  - `aura.corpus.ingest`

## Supported Inputs
Media: MP4, MOV, MKV, WEBM, AVI, WAV, MP3, M4A, AAC, FLAC, OGG, OPUS.
Transcript/text: TXT, TFT, SRT, VTT, MD, JSON, CSV, TSV.

## Core Pipeline
1. Inspect source and record immutable evidence/hash.
2. If media, extract 16 kHz mono PCM audio with FFmpeg.
3. Transcribe locally through configured `whisper.cpp` CLI.
4. Preserve original terminology and acronyms exactly when recognized.
5. Segment statements and classify each as `serious`, `humor`, `mixed`, `serious_candidate` or `ambiguous`.
6. Use only high-confidence serious statements as direct input to critical analysis.
7. Keep humor/mixed/ambiguous statements in separate evidence lanes so context is not lost.
8. Run critical-thinking governance over serious findings, contradictions, decisions, risks and action items.
9. Produce analysis with timestamps/speaker references when available from the source transcript.

## Terminology Preservation
Never translate or expand established technical/business terms merely to localize the transcript. Preserve forms such as `end-to-end`, `E2E`, `B2B`, `B2C`, `API`, `REST`, `GraphQL`, `gRPC`, `Node.js`, `JavaScript`, `TypeScript`, `React`, `Angular`, `AWS`, `CI/CD`, `RAG`, `LLM`, `MCP`, `LSP`, `OAuth`, `JWT`, `frontend`, `backend`, `rollback`, `deploy`, `throughput`, `latency`, `observability` and other domain-native nomenclature when that wording appears in speech/source evidence.

Do not transform `end-to-end` into `fim a fim`, `B2C` into `business-to-consumer`/`negócio para consumidor`, or analogous terminology unless the speaker explicitly expands or translates it.

## Humor and Semantic Policy
Humor detection is a filtering signal, not deletion. A segment classified as humor must remain traceable but is excluded from serious claims unless another independent serious segment supports the same claim.

Signals include laughter markers, explicit joke markers, exaggeration, wordplay, irony/sarcasm cues and contradiction with surrounding serious context. Deterministic lexical rules are first-pass only. Ambiguous/mixed cases must remain `ambiguous` or `mixed`; they MUST NOT be promoted to serious facts without semantic corroboration.

## Speaker Recognition / Diarization
When source subtitles/transcripts contain speaker labels, preserve them. When the configured ASR/diarization backend produces speaker IDs, maintain stable `SPEAKER_n` identities within the recording. Never infer real-world identity from voice alone unless explicitly mapped by the operator.

## Serious Analysis Output
- facts stated seriously
- decisions and commitments
- architecture/technical claims
- requirements
- risks and objections
- contradictions
- root causes
- action items and ownership if stated
- deadlines/dates if stated
- assumptions explicitly distinguished from facts
- unresolved ambiguity
- confidence and evidence reference for each finding

## Learning / Semantic Corpus
`aura.corpus.ingest` may build a governed semantic corpus from local or YouTube-derived transcripts ONLY when the operator attests authorization/licensing with `authorized=true` and records source/provenance. This corpus is for retrieval/evaluation/calibration; ingestion does not by itself constitute model weight training.

For YouTube, do not bypass access controls, download private/restricted media, or mass-scrape transcripts. Accept operator-provided/licensed media/transcripts or an officially accessible/exported transcript. Store source URI, language, authorization note, timestamp and content hash.

## Determinism Contract
- same transcript + same tool version + same policy => same first-pass classification;
- no stochastic rewriting before evidence hashing;
- technical terms preserved before analysis;
- high-confidence serious lane separated from humor and ambiguity;
- all promotions from ambiguous/mixed to serious require explicit evidence from the critical-thinking layer.

## Privacy and Security
Recorded conversations may contain confidential, personal or credential information. Do not persist secrets into reports/memory. Redact passwords/tokens/keys and minimize sensitive personal data. Do not perform speaker identity inference or biometric matching.

## Stop Conditions
- source is unauthorized or provenance is unknown for corpus learning;
- media/transcript path is outside the authorized workspace;
- required FFmpeg/whisper backend is unavailable for requested transcription;
- transcript quality is too low to support the requested conclusion;
- humor/serious intent remains materially ambiguous;
- analysis would require inventing omitted words, speakers or context.

## Output Schema
```json
{
  "status": "PASS|WARN|BLOCKED",
  "source": {},
  "transcript": {"language": "", "hash": "", "path": ""},
  "segments": [],
  "serious_findings": [],
  "humor_segments": [],
  "ambiguous_segments": [],
  "contradictions": [],
  "decisions": [],
  "risks": [],
  "action_items": [],
  "terminology_preserved": [],
  "confidence": 0.0,
  "evidence_refs": []
}
```
