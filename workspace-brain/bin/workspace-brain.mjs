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
import { readSessionBootstrap, rebuildSessionBootstrap } from "../src/memory-layers.mjs";
import { upsertNote, readNote } from "../src/notes.mjs";
import { upsertWikiPage, wikiStats } from "../src/wiki.mjs";
import { runDream } from "../src/dream.mjs";

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
  dream [--llm]        Consolida memória (bootstrap + opcional DeepSeek)
  bootstrap            Reconstrói memory/session/BOOTSTRAP.md
  memory-stats         Estatísticas wiki/notes
  note ...             Cria nota (flags --title --rule --evidence --pitfalls)
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
    else if (a === "--title") flags.title = args[++i];
    else if (a === "--rule") flags.rule = args[++i];
    else if (a === "--evidence") flags.evidence = args[++i];
    else if (a === "--pitfalls") flags.pitfalls = args[++i];
    else if (a === "--links") flags.links = args[++i];
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

  if (cmd === "dream") {
    const useLlm = rest.includes("--llm");
    console.log(JSON.stringify(await runDream({ useLlm }), null, 2));
    return;
  }

  if (cmd === "bootstrap") {
    console.log(JSON.stringify(rebuildSessionBootstrap(), null, 2));
    return;
  }

  if (cmd === "memory-stats") {
    console.log(JSON.stringify({ wiki: wikiStats(), bootstrap_lines: readSessionBootstrap().split("\n").length }, null, 2));
    return;
  }

  if (cmd === "note") {
    const { flags } = parseFlags(rest);
    if (!flags.title || !flags.rule) throw new Error("note --title X --rule Y --evidence a,b");
    const evidence = (flags.evidence ?? "").split(",").map((s) => s.trim()).filter(Boolean);
    const pitfalls = (flags.pitfalls ?? "").split(",").map((s) => s.trim()).filter(Boolean);
    console.log(JSON.stringify(upsertNote({ title: flags.title, rule: flags.rule, evidence, pitfalls }), null, 2));
    rebuildSessionBootstrap();
    return;
  }

  if (cmd === "wiki") {
    const { flags, positional } = parseFlags(rest);
    const title = flags.title ?? positional[0];
    const summary = flags.summary ?? positional.slice(1).join(" ");
    if (!title || !summary) throw new Error("wiki --title X --summary Y");
    console.log(JSON.stringify(upsertWikiPage({ title, summary, links: (flags.links ?? "").split(",").filter(Boolean) }), null, 2));
    rebuildSessionBootstrap();
    return;
  }

  console.error(`Comando desconhecido: ${cmd}\n${usage()}`);
  process.exit(1);
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : err);
  process.exit(1);
});
