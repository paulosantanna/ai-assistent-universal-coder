#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync, appendFileSync } from 'node:fs';
import { extname, dirname, resolve } from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);
const MAX_TEXT_BYTES = 8 * 1024 * 1024;
const MAX_ANALYSIS_SEGMENTS = 5000;
const SUPPORTED_TEXT = new Set(['.txt','.tft','.srt','.vtt','.md','.json','.csv','.tsv']);
const SUPPORTED_MEDIA = new Set(['.mp4','.mov','.mkv','.webm','.avi','.wav','.mp3','.m4a','.aac','.flac','.ogg','.opus']);
const TECH_TERMS = [
  'end-to-end','e2e','b2b','b2c','api','rest','graphql','grpc','http','https','json','yaml','xml','sql','nosql','node.js','node','javascript','typescript','react','angular','java','spring boot','aws','azure','gcp','kubernetes','docker','ci/cd','devops','sre','rag','llm','mcp','lsp','oauth','jwt','webhook','frontend','backend','full-stack','microservice','microservices','cache','latency','throughput','rollback','deploy','deployment','observability','open telemetry','opentelemetry'
];
const STRONG_HUMOR_MARKERS = [
  /\b(t[oô] brincando|estou brincando|era brincadeira|s[oó] brincadeira|just kidding|i(?:'|’)m kidding|only kidding)\b/i,
  /\[(risos?|laughter|laughs?)\]/i
];
const HUMOR_MARKERS = [
  ...STRONG_HUMOR_MARKERS,
  /\b(brincadeira|zoeira|zuera|piada|risos?|kkkk+|haha+|rsrs+)\b/i,
  /\b(kidding|joke|laughs?|lol|lmao)\b/i
];
const SERIOUS_MARKERS = [
  /\b(precisamos|devemos|obrigatório|risco|incidente|produção|production|security|segurança|deadline|prazo|arquitetura|architecture|bug|erro|error|falha|failure|deploy|database|banco de dados|custo|cost|cliente|customer|requisito|requirement)\b/i,
  /\b(i think|we need|we must|should|must|require|risk|incident|issue|root cause|decision|proposal|recommend)\b/i
];

function sha256(text) { return createHash('sha256').update(text).digest('hex'); }
function bounded(text, max = MAX_TEXT_BYTES) { return Buffer.byteLength(text) <= max ? text : Buffer.from(text).subarray(0, max).toString('utf8'); }
function ensureParent(path) { mkdirSync(dirname(path), { recursive: true }); }
function cleanError(error) {
  const text = String(error?.stderr || error?.message || error || 'unknown error');
  return text.replace(/(?:password|token|secret|key)\s*[:=]\s*\S+/gi, '$1=***REDACTED***').slice(0, 1200);
}
function parseSubtitle(text) {
  return text
    .replace(/^WEBVTT.*$/gmi, '')
    .replace(/^\d+\s*$/gm, '')
    .replace(/^\s*\d\d:\d\d(?::\d\d)?[.,]\d+\s+-->\s+.*$/gm, '')
    .replace(/<[^>]+>/g, '')
    .replace(/\r/g, '')
    .split('\n')
    .map(x => x.trim())
    .filter(Boolean)
    .join('\n');
}
function readTranscript(path) {
  if (!existsSync(path)) throw new Error(`File not found: ${path}`);
  const ext = extname(path).toLowerCase();
  if (!SUPPORTED_TEXT.has(ext)) throw new Error(`Unsupported transcript format: ${ext}`);
  const raw = bounded(readFileSync(path, 'utf8'));
  if (ext === '.srt' || ext === '.vtt') return parseSubtitle(raw);
  if (ext === '.json') {
    const value = JSON.parse(raw);
    if (Array.isArray(value)) return value.map(x => typeof x === 'string' ? x : x?.text ?? JSON.stringify(x)).join('\n');
    if (typeof value?.text === 'string') return value.text;
    if (Array.isArray(value?.segments)) return value.segments.map(x => x?.text ?? '').join('\n');
    return JSON.stringify(value, null, 2);
  }
  return raw;
}
function preserveTerms(original, normalized) {
  let out = normalized;
  for (const term of TECH_TERMS) {
    const re = new RegExp(`\\b${term.replace(/[.*+?^${}()|[\\]\\]/g, '\\$&')}\\b`, 'ig');
    const originalHit = original.match(re)?.[0];
    if (originalHit) out = out.replace(re, originalHit);
  }
  return out;
}
function classifySegment(text) {
  const strongHumor = STRONG_HUMOR_MARKERS.some(re => re.test(text));
  const humor = HUMOR_MARKERS.some(re => re.test(text));
  const serious = SERIOUS_MARKERS.some(re => re.test(text));
  let label = 'ambiguous';
  let confidence = 0.5;

  // Explicit self-disambiguation such as "tô brincando" / "just kidding" has
  // higher semantic authority than incidental serious vocabulary inside the joke.
  if (strongHumor) { label = 'humor'; confidence = 0.96; }
  else if (humor && !serious) { label = 'humor'; confidence = 0.88; }
  else if (serious && !humor) { label = 'serious'; confidence = 0.84; }
  else if (serious && humor) { label = 'mixed'; confidence = 0.66; }
  else if (/[.!?]$/.test(text) && text.split(/\s+/).length >= 8) { label = 'serious_candidate'; confidence = 0.58; }
  return { label, confidence, humor_signal: humor, strong_humor_signal: strongHumor, serious_signal: serious };
}
function analyzeTranscript(text) {
  const lines = text.split(/\n+|(?<=[.!?])\s+(?=[A-ZÀ-Ú0-9])/u).map(x => x.trim()).filter(Boolean).slice(0, MAX_ANALYSIS_SEGMENTS);
  const segments = lines.map((raw, index) => {
    const normalized = preserveTerms(raw, raw.replace(/\s+/g, ' ').trim());
    return { index, text: normalized, ...classifySegment(normalized) };
  });
  const serious = segments.filter(s => s.label === 'serious' || (s.label === 'serious_candidate' && s.confidence >= 0.6));
  const humor = segments.filter(s => s.label === 'humor');
  const ambiguous = segments.filter(s => !serious.includes(s) && !humor.includes(s));
  return {
    language_policy: 'preserve-original-technical-terms',
    deterministic_policy: 'high-confidence-serious-only',
    segments,
    serious_segments: serious,
    humor_segments: humor,
    ambiguous_segments: ambiguous,
    serious_text: serious.map(s => s.text).join('\n'),
    statistics: { total: segments.length, serious: serious.length, humor: humor.length, ambiguous: ambiguous.length }
  };
}
async function inspectMedia(path) {
  if (!existsSync(path)) throw new Error(`File not found: ${path}`);
  if (!SUPPORTED_MEDIA.has(extname(path).toLowerCase())) throw new Error('Unsupported media format');
  const ffprobe = process.env.AURA_FFPROBE_BIN || 'ffprobe';
  const { stdout } = await execFileAsync(ffprobe, ['-v','error','-show_entries','format=duration,size,bit_rate:stream=index,codec_type,codec_name,sample_rate,channels,width,height','-of','json',path], { maxBuffer: 2 * 1024 * 1024 });
  return JSON.parse(stdout);
}
async function extractAudio(input, output) {
  if (!existsSync(input)) throw new Error(`File not found: ${input}`);
  ensureParent(output);
  const ffmpeg = process.env.AURA_FFMPEG_BIN || 'ffmpeg';
  await execFileAsync(ffmpeg, ['-y','-i',input,'-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',output], { maxBuffer: 4 * 1024 * 1024 });
  return { output, format: 'wav', sample_rate: 16000, channels: 1 };
}
async function transcribeLocal(input, outputPrefix, language = 'auto') {
  if (!existsSync(input)) throw new Error(`File not found: ${input}`);
  const whisper = process.env.AURA_WHISPER_BIN || 'whisper-cli';
  const model = process.env.AURA_WHISPER_MODEL;
  if (!model) throw new Error('AURA_WHISPER_MODEL is required for local transcription');
  ensureParent(outputPrefix);
  const args = ['-m', model, '-f', input, '-otxt', '-osrt', '-ovtt', '-of', outputPrefix, '--print-progress', 'false'];
  if (language && language !== 'auto') args.push('-l', language);
  await execFileAsync(whisper, args, { maxBuffer: 16 * 1024 * 1024, timeout: Number(process.env.AURA_TRANSCRIBE_TIMEOUT_MS || 3600000) });
  const txtPath = `${outputPrefix}.txt`;
  if (!existsSync(txtPath)) throw new Error('whisper.cpp completed without producing transcript');
  const text = bounded(readFileSync(txtPath, 'utf8'));
  return { text, txt: txtPath, srt: `${outputPrefix}.srt`, vtt: `${outputPrefix}.vtt`, language };
}
function ingestCorpus(params) {
  if (params.authorized !== true) throw new Error('Corpus ingestion requires authorized=true');
  if (!params.source || !params.path) throw new Error('source and path are required');
  const text = readTranscript(params.path);
  const analysis = analyzeTranscript(text);
  const corpusPath = resolve(params.corpus_path || '.aeos/aura-voice/corpus.jsonl');
  ensureParent(corpusPath);
  const record = {
    id: sha256(`${params.source}\n${text}`),
    source: params.source,
    source_type: params.source_type || 'local',
    language: params.language || 'unknown',
    license_or_authorization: params.license_or_authorization || 'operator-attested',
    ingested_at: new Date().toISOString(),
    content_hash: sha256(text),
    serious_samples: analysis.serious_segments.map(x => x.text),
    humor_samples: analysis.humor_segments.map(x => x.text),
    ambiguous_samples: analysis.ambiguous_segments.map(x => x.text)
  };
  appendFileSync(corpusPath, JSON.stringify(record) + '\n', 'utf8');
  return { corpus_path: corpusPath, record_id: record.id, counts: analysis.statistics };
}
async function handle(action, params = {}) {
  switch (action) {
    case 'aura.health': return { version: '1.0.1', media: [...SUPPORTED_MEDIA], transcripts: [...SUPPORTED_TEXT], asr: 'whisper.cpp', extraction: 'ffmpeg' };
    case 'aura.media.inspect': return inspectMedia(String(params.path || ''));
    case 'aura.media.extract_audio': return extractAudio(String(params.input || ''), String(params.output || ''));
    case 'aura.transcript.read': { const text = readTranscript(String(params.path || '')); return { text, hash: sha256(text) }; }
    case 'aura.transcribe.local': return transcribeLocal(String(params.input || ''), String(params.output_prefix || '.aeos/aura-voice/transcript'), String(params.language || 'auto'));
    case 'aura.analyze.transcript': { const text = params.text ? String(params.text) : readTranscript(String(params.path || '')); return analyzeTranscript(text); }
    case 'aura.corpus.ingest': return ingestCorpus(params);
    default: throw new Error(`Unknown Aura Voice action: ${action}`);
  }
}

let buffer = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => {
  buffer += chunk;
  let idx;
  while ((idx = buffer.indexOf('\n')) >= 0) {
    const line = buffer.slice(0, idx).trim(); buffer = buffer.slice(idx + 1);
    if (!line) continue;
    Promise.resolve().then(async () => {
      let request;
      try { request = JSON.parse(line); const data = await handle(request.action, request.params || {}); process.stdout.write(JSON.stringify({ request_id: request.request_id, success: true, data }) + '\n'); }
      catch (error) { process.stdout.write(JSON.stringify({ request_id: request?.request_id, success: false, error: cleanError(error) }) + '\n'); }
    });
  }
});
process.on('SIGTERM', () => process.exit(0));
