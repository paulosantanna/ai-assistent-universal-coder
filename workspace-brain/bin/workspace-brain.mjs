#!/usr/bin/env node
import { ensureLayout, paths, getBrainRoot } from "../src/paths.mjs";
import { walkIngest, searchCorpus, corpusStats } from "../src/corpus.mjs";
import { brainAsk } from "../src/rag.mjs";
import { ingestUrl, mapSeedUrls } from "../src/url-map.mjs";
import { recordEvent } from "../src/events.mjs";
import { writeIngestManifest, readLatestManifest } from "../src/manifest.mjs";
import { installAgentSnippets } from "../src/install-agents.mjs";
import { getDeepSeekApiKey, getTypesafeApiKey, resolveUniversalCoderRoot } from "../src/config.mjs";
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const [, , cmd, ...rest] = process.argv;

function usage() {
  return `workspace-brain (wb) — MCP + CLI

Comandos:
  init                 Cria layout em WORKSPACE_BRAIN_ROOT
  doctor               Verifica caminhos e credenciais (sem expor segredos)
  ingest <dir>         Ingere diretório
  ingest-url <url>     Ingere URL (Jev)
  map-seeds [urls...]  Ingere seeds GitHub do universal-coder ou URLs
  search <query>       Busca no corpus
  ask <pergunta>       RAG DeepSeek
  event --tool X ...   Regista evento NDJSON
  manifest             Mostra manifesto
  install-agents       Gera snippets MCP em config/
  mcp                  Inicia servidor MCP (stdio)

Variáveis: WORKSPACE_BRAIN_ROOT, JEV_CONFIG_DIR, DEEPSEEK_API_KEY, UNIVERSAL_CODER_ROOT
`;
}

function parseFlags(args) {
  const flags = {};
  const positional = [];
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === "--force") flags.force = true;
    else if (a === "--tool") flags.tool = args[++i];
    else if (a === "--action") flags.action = args[++i];
    else if (a === "--paths") flags.paths = args[++i].split(",").map((s) => s.trim());
    else if (a === "--summary") flags.summary = args[++i];
    else positional.push(a);
  }
  return { flags, positional };
}

async function main() {
  if (!cmd || cmd === "help" || cmd === "-h") {
    console.log(usage());
    return;
  }

  if (cmd === "mcp") {
    const { startMcpServer } = await import("../src/mcp-server.mjs");
    await startMcpServer();
    return;
  }

  ensureLayout();

  if (cmd === "init") {
    console.log(JSON.stringify({ brain_root: getBrainRoot(), layout: paths() }, null, 2));
    return;
  }

  if (cmd === "doctor") {
    const root = getBrainRoot();
    console.log(
      JSON.stringify(
        {
          brain_root: root,
          layout_ok: existsSync(join(root, "corpus")),
          deepseek_configured: Boolean(getDeepSeekApiKey()),
          jev_typesafe_configured: Boolean(getTypesafeApiKey()),
          universal_coder_root: resolveUniversalCoderRoot() ?? null,
          ...corpusStats(),
        },
        null,
        2,
      ),
    );
    return;
  }

  if (cmd === "ingest") {
    const dir = rest[0];
    if (!dir) throw new Error("Uso: ingest <dir>");
    const n = walkIngest(dir);
    const m = writeIngestManifest({ source: { type: "path", path: dir }, counts: { last_ingest_chunks: n.length } });
    console.log(JSON.stringify({ ingested: n.length, manifest_id: m.dataset_id }, null, 2));
    return;
  }

  if (cmd === "ingest-url") {
    const url = rest[0];
    const { flags } = parseFlags(rest.slice(1));
    if (!url) throw new Error("Uso: ingest-url <url> [--force]");
    console.log(JSON.stringify(await ingestUrl(url, { force: flags.force }), null, 2));
    return;
  }

  if (cmd === "map-seeds") {
    const { flags, positional } = parseFlags(rest);
    let urls = positional.filter((u) => u.startsWith("http"));
    if (!urls.length) {
      const uroot = resolveUniversalCoderRoot();
      const readme = uroot && join(uroot, "07_mapeamentos", "repositorios-skills", "README.md");
      if (readme && existsSync(readme)) {
        const md = readFileSync(readme, "utf8");
        urls = [...new Set([...md.matchAll(/https:\/\/github\.com\/[^\s)]+/g)].map((m) => m[0]))].slice(0, 20);
      }
    }
    console.log(JSON.stringify(await mapSeedUrls(urls, { force: flags.force }), null, 2));
    return;
  }

  if (cmd === "search") {
    const q = rest.join(" ").trim();
    console.log(JSON.stringify(searchCorpus(q), null, 2));
    return;
  }

  if (cmd === "ask") {
    const q = rest.join(" ").trim();
    console.log(JSON.stringify(await brainAsk(q), null, 2));
    return;
  }

  if (cmd === "event") {
    const { flags } = parseFlags(rest);
    console.log(
      JSON.stringify(
        recordEvent({
          tool: flags.tool ?? "cli",
          action: flags.action ?? "change",
          paths: flags.paths ?? [],
          summary: flags.summary ?? "",
        }),
        null,
        2,
      ),
    );
    return;
  }

  if (cmd === "manifest") {
    console.log(JSON.stringify(readLatestManifest() ?? { empty: true }, null, 2));
    return;
  }

  if (cmd === "install-agents") {
    console.log(JSON.stringify(installAgentSnippets(), null, 2));
    return;
  }

  console.error(`Comando desconhecido: ${cmd}\n${usage()}`);
  process.exit(1);
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : err);
  process.exit(1);
});
