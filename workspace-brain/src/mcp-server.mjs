import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { ensureLayout, paths, getBrainRoot } from "./paths.mjs";
import { walkIngest, searchCorpus, corpusStats } from "./corpus.mjs";
import { brainAsk } from "./rag.mjs";
import { ingestUrl, mapSeedUrls } from "./url-map.mjs";
import { recordEvent } from "./events.mjs";
import { readLatestManifest, writeIngestManifest } from "./manifest.mjs";
import { resolveUniversalCoderRoot } from "./config.mjs";
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

function textResult(obj) {
  return { content: [{ type: "text", text: typeof obj === "string" ? obj : JSON.stringify(obj, null, 2) }] };
}

function seedsFromUniversalCoder() {
  const root = resolveUniversalCoderRoot();
  if (!root) return [];
  const readme = join(root, "07_mapeamentos", "repositorios-skills", "README.md");
  if (!existsSync(readme)) return [];
  const md = readFileSync(readme, "utf8");
  const urls = [...md.matchAll(/https:\/\/github\.com\/[^\s)]+/g)].map((m) => m[0]);
  return [...new Set(urls)].slice(0, 20);
}

export async function startMcpServer() {
  ensureLayout();
  const server = new McpServer({ name: "workspace-brain", version: "0.1.0" });

  server.tool("brain_health", "Status do cérebro e caminhos.", async () => {
    const p = paths();
    return textResult({
      ok: true,
      brain_root: getBrainRoot(),
      ...corpusStats(),
      manifest: readLatestManifest()?.dataset_id ?? null,
      events: p.events,
    });
  });

  server.tool(
    "brain_search",
    "Busca lexical/BM25 no corpus local (armazenamento em disco).",
    { query: z.string(), top_k: z.number().int().min(1).max(30).optional() },
    async ({ query, top_k }) => textResult(searchCorpus(query, { topK: top_k ?? 8 })),
  );

  server.tool(
    "brain_ask",
    "RAG: recupera chunks e responde via DeepSeek (nuvem).",
    { question: z.string(), top_k: z.number().int().min(1).max(20).optional() },
    async ({ question, top_k }) => textResult(await brainAsk(question, { topK: top_k ?? 6 })),
  );

  server.tool(
    "brain_ingest_path",
    "Ingere ficheiros de texto de um diretório no corpus.",
    { path: z.string(), source: z.string().optional() },
    async ({ path, source }) => {
      const n = walkIngest(path, { source: source ?? "repo" });
      const manifest = writeIngestManifest({ source: { type: "path", path }, counts: { last_ingest_chunks: n.length } });
      return textResult({ ingested: n.length, manifest_id: manifest.dataset_id });
    },
  );

  server.tool(
    "brain_ingest_url",
    "Ingere URL após julgamento Jev (ou heurística).",
    { url: z.string().url(), force: z.boolean().optional() },
    async ({ url, force }) => textResult(await ingestUrl(url, { force: force ?? false })),
  );

  server.tool(
    "brain_map_seeds",
    "Mapeia seeds (URLs explícitas ou README do universal-coder).",
    { urls: z.array(z.string().url()).optional(), force: z.boolean().optional() },
    async ({ urls, force }) => {
      const list = urls?.length ? urls : seedsFromUniversalCoder();
      if (!list.length) {
        return textResult({ ok: false, error: "Sem URLs. Passe urls[] ou defina UNIVERSAL_CODER_ROOT." });
      }
      return textResult(await mapSeedUrls(list, { force: force ?? false }));
    },
  );

  server.tool(
    "brain_record_event",
    "Regista alteração feita por Cursor/Codex/OpenCode/Claude/etc.",
    {
      tool: z.string(),
      action: z.string(),
      paths: z.array(z.string()).optional(),
      summary: z.string().optional(),
    },
    async (args) => textResult(recordEvent(args)),
  );

  server.tool("brain_manifest", "Último manifesto de ingestão.", async () => textResult(readLatestManifest() ?? { empty: true }));

  const transport = new StdioServerTransport();
  await server.connect(transport);
}

if (process.argv[1]?.endsWith("mcp-server.mjs")) {
  startMcpServer().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}
