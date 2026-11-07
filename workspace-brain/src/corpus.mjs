import { createHash } from "node:crypto";
import { readFileSync, writeFileSync, existsSync, readdirSync } from "node:fs";
import { join, relative } from "node:path";
import { paths } from "./paths.mjs";

const DEFAULT_CHUNK = 1400;
const SKIP_DIRS = new Set([
  "node_modules",
  ".git",
  "dist",
  "build",
  ".next",
  "coverage",
  "__pycache__",
]);
const TEXT_EXT = new Set([
  ".md",
  ".txt",
  ".json",
  ".yaml",
  ".yml",
  ".mjs",
  ".js",
  ".ts",
  ".tsx",
  ".jsx",
  ".py",
  ".java",
  ".cs",
  ".go",
  ".rs",
  ".html",
  ".css",
  ".sql",
  ".sh",
  ".ps1",
]);

function sha256(text) {
  return createHash("sha256").update(text).digest("hex");
}

function loadIndex(p) {
  if (!existsSync(p.index)) return { version: 1, chunks: [] };
  return JSON.parse(readFileSync(p.index, "utf8"));
}

function saveIndex(p, index) {
  writeFileSync(p.index, JSON.stringify(index, null, 2) + "\n", "utf8");
}

export function chunkText(text, size = DEFAULT_CHUNK) {
  const parts = [];
  for (let i = 0; i < text.length; i += size) {
    parts.push(text.slice(i, i + size));
  }
  return parts.filter((s) => s.trim().length > 0);
}

export function ingestChunk({ text, source, sourcePath, url, meta = {} }) {
  const p = paths();
  const index = loadIndex(p);
  const id = sha256(`${source}|${sourcePath}|${text.slice(0, 200)}`);
  const record = {
    id,
    text,
    source,
    sourcePath: sourcePath ?? null,
    url: url ?? null,
    sha256: sha256(text),
    createdAt: new Date().toISOString(),
    ...meta,
  };
  writeFileSync(join(p.chunks, `${id}.json`), JSON.stringify(record, null, 2) + "\n", "utf8");
  if (!index.chunks.find((c) => c.id === id)) {
    index.chunks.push({ id, source, sourcePath, url, sha256: record.sha256, createdAt: record.createdAt });
  }
  saveIndex(p, index);
  return record;
}

export function ingestFile(filePath, { source = "file", baseDir } = {}) {
  const rel = baseDir ? relative(baseDir, filePath) : filePath;
  const text = readFileSync(filePath, "utf8");
  const chunks = chunkText(text);
  return chunks.map((part, i) =>
    ingestChunk({
      text: part,
      source,
      sourcePath: rel,
      meta: { part: i, parts: chunks.length },
    }),
  );
}

export function walkIngest(dir, options = {}) {
  const { source = "repo", exts = TEXT_EXT } = options;
  const ingested = [];
  function walk(current) {
    let entries;
    try {
      entries = readdirSync(current, { withFileTypes: true });
    } catch {
      return;
    }
    for (const ent of entries) {
      const full = join(current, ent.name);
      if (ent.isDirectory()) {
        if (SKIP_DIRS.has(ent.name)) continue;
        walk(full);
        continue;
      }
      const ext = ent.name.includes(".") ? ent.name.slice(ent.name.lastIndexOf(".")).toLowerCase() : "";
      if (!exts.has(ext)) continue;
      if (ent.name.length > 200) continue;
      try {
        const st = readFileSync(full);
        if (st.length > 2_000_000) continue;
        ingested.push(...ingestFile(full, { source, baseDir: dir }));
      } catch {
        /* binary or encoding */
      }
    }
  }
  walk(dir);
  return ingested;
}

export function loadAllChunks() {
  const p = paths();
  const index = loadIndex(p);
  const out = [];
  for (const ref of index.chunks) {
    const file = join(p.chunks, `${ref.id}.json`);
    if (!existsSync(file)) continue;
    out.push(JSON.parse(readFileSync(file, "utf8")));
  }
  return out;
}

function tokenize(s) {
  return s
    .toLowerCase()
    .replace(/[^\p{L}\p{N}_./-]+/gu, " ")
    .split(/\s+/)
    .filter(Boolean);
}

/** BM25 simplificado em memória (determinístico para o corpus atual). */
export function searchCorpus(query, { topK = 8 } = {}) {
  const docs = loadAllChunks();
  const qTerms = tokenize(query);
  if (!docs.length || !qTerms.length) return [];

  const df = new Map();
  const docTerms = docs.map((d) => {
    const terms = tokenize(d.text);
    const tf = new Map();
    for (const t of terms) tf.set(t, (tf.get(t) ?? 0) + 1);
    for (const t of tf.keys()) df.set(t, (df.get(t) ?? 0) + 1);
    return { doc: d, tf, len: terms.length };
  });

  const N = docs.length;
  const k1 = 1.2;
  const b = 0.75;
  const avgdl = docTerms.reduce((a, x) => a + x.len, 0) / N || 1;

  const scored = docTerms.map(({ doc, tf, len }) => {
    let score = 0;
    for (const term of qTerms) {
      const n = tf.get(term) ?? 0;
      if (!n) continue;
      const idf = Math.log(1 + (N - (df.get(term) ?? 0) + 0.5) / ((df.get(term) ?? 0) + 0.5));
      score += idf * ((n * (k1 + 1)) / (n + k1 * (1 - b + (b * len) / avgdl)));
    }
    return { ...doc, score };
  });

  return scored
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, topK)
    .map(({ id, text, source, sourcePath, url, score, sha256: digest }) => ({
      id,
      score,
      source,
      sourcePath,
      url,
      sha256: digest,
      excerpt: text.length > 400 ? `${text.slice(0, 400)}…` : text,
      text,
    }));
}

export function corpusStats() {
  const p = paths();
  const index = loadIndex(p);
  return { chunk_count: index.chunks.length, index_path: p.index };
}
