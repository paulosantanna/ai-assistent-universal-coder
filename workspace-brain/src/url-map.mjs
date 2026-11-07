import { assessUrlForIngest } from "./jev.mjs";
import { ingestChunk } from "./corpus.mjs";
import { writeIngestManifest } from "./manifest.mjs";

const MAX_BYTES = 500_000;
const FETCH_TIMEOUT = 25_000;

function stripHtml(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

export async function fetchUrlText(url) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), FETCH_TIMEOUT);
  try {
    const res = await fetch(url, {
      signal: ctrl.signal,
      headers: { "User-Agent": "workspace-brain/0.1 (+https://github.com/paulosantanna/ai-assistent-universal-coder)" },
    });
    const buf = await res.arrayBuffer();
    if (buf.byteLength > MAX_BYTES) throw new Error(`Resposta maior que ${MAX_BYTES} bytes`);
    const text = new TextDecoder("utf-8", { fatal: false }).decode(buf);
    return { status: res.status, contentType: res.headers.get("content-type"), text };
  } finally {
    clearTimeout(t);
  }
}

export async function ingestUrl(url, { force = false } = {}) {
  const gate = await assessUrlForIngest(url);
  if (!gate.include && !force) {
    return { ok: false, gate, ingested: 0 };
  }
  const { text, contentType } = await fetchUrlText(url);
  const plain = contentType?.includes("html") ? stripHtml(text) : text;
  const titleMatch = text.match(/<title[^>]*>([^<]+)<\/title>/i);
  const chunks = [];
  const parts = plain.length > 1400 ? plain.match(/.{1,1400}/gs) ?? [plain] : [plain];
  for (let i = 0; i < parts.length; i++) {
    chunks.push(
      ingestChunk({
        text: parts[i],
        source: "web",
        sourcePath: url,
        url,
        meta: { part: i, contentType, gate },
      }),
    );
  }
  const manifest = writeIngestManifest({
    source: { type: "url", url },
    counts: { last_ingest_chunks: chunks.length },
    notes: [`jev_mode=${gate.mode}`, `choice=${gate.choice}`],
  });
  return { ok: true, gate, ingested: chunks.length, manifest_id: manifest.dataset_id };
}

export async function mapSeedUrls(urls, { force = false } = {}) {
  const results = [];
  for (const url of urls) {
    try {
      results.push({ url, ...(await ingestUrl(url, { force })) });
    } catch (err) {
      results.push({ url, ok: false, error: err instanceof Error ? err.message : String(err) });
    }
  }
  return results;
}
