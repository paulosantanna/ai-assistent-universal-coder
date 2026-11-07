import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

process.env.WORKSPACE_BRAIN_ROOT = mkdtempSync(join(tmpdir(), "wb-smoke-"));

const { ensureLayout } = await import("../src/paths.mjs");
const { ingestChunk, searchCorpus } = await import("../src/corpus.mjs");
const { recordEvent } = await import("../src/events.mjs");
const { installAgentSnippets } = await import("../src/install-agents.mjs");

try {
  ensureLayout();
  ingestChunk({ text: "workspace brain smoke test codenavi", source: "test", sourcePath: "smoke.md" });
  const hits = searchCorpus("codenavi smoke");
  if (!hits.length) throw new Error("search failed");
  recordEvent({ tool: "cli", action: "smoke", paths: ["smoke.md"], summary: "ok" });
  const snippets = installAgentSnippets();
  if (!snippets.written.length) throw new Error("install-agents failed");
  console.log(JSON.stringify({ ok: true, hits: hits.length, snippets: snippets.written.length }));
} finally {
  rmSync(process.env.WORKSPACE_BRAIN_ROOT, { recursive: true, force: true });
}
