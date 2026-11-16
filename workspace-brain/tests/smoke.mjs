import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

process.env.WORKSPACE_BRAIN_ROOT = mkdtempSync(join(tmpdir(), "wb-smoke-"));

const { ensureLayout } = await import("../src/paths.mjs");
const { ingestChunk, searchCorpus } = await import("../src/corpus.mjs");
const { recordEvent } = await import("../src/events.mjs");
const { installAgentSnippets } = await import("../src/install-agents.mjs");
const { upsertNote } = await import("../src/notes.mjs");
const { runDream } = await import("../src/dream.mjs");
const { readSessionBootstrap } = await import("../src/memory-layers.mjs");

try {
  ensureLayout();
  ingestChunk({ text: "workspace brain smoke test codenavi", source: "test", sourcePath: "smoke.md" });
  const hits = searchCorpus("codenavi smoke");
  if (!hits.length) throw new Error("search failed");
  recordEvent({ tool: "cli", action: "smoke", paths: ["smoke.md"], summary: "ok" });
  const snippets = installAgentSnippets();
  if (!snippets.written.length) throw new Error("install-agents failed");
  upsertNote({
    title: "Smoke note",
    rule: "Dream rebuilds bootstrap",
    evidence: ["smoke:test"],
    pitfalls: ["notes without evidence are rejected"],
  });
  await runDream({ useLlm: false });
  const boot = readSessionBootstrap();
  if (!boot.includes("Smoke note")) throw new Error("bootstrap missing note");
  console.log(JSON.stringify({ ok: true, hits: hits.length, snippets: snippets.written.length, bootstrap_lines: boot.split("\n").length }));
} finally {
  rmSync(process.env.WORKSPACE_BRAIN_ROOT, { recursive: true, force: true });
}
