import { writeFileSync, readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { createHash } from "node:crypto";
import { ensureMemoryLayout, memoryPaths } from "./memory-layers.mjs";

const WIKI_WARN_BYTES = 2_000_000;

function slug(title) {
  const base = title
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 48);
  const hash = createHash("sha256").update(title).digest("hex").slice(0, 6);
  return `${base || "page"}-${hash}`;
}

export function upsertWikiPage({ title, summary, links = [], body = "" }) {
  if (!title?.trim() || !summary?.trim()) throw new Error("title e summary são obrigatórios");
  const m = ensureMemoryLayout();
  const id = slug(title);
  const path = join(m.wiki, `${id}.md`);
  const linkLines = links.map((l) => (l.startsWith("[[") ? l : `[[${l}]]`));
  const content = [
    `# ${title}`,
    "",
    summary.trim(),
    "",
    linkLines.length ? "## Ligações\n" + linkLines.map((l) => `- ${l}`).join("\n") + "\n" : "",
    body.trim() ? `## Detalhe\n${body.trim()}\n` : "",
    "> Wiki deve resumir e ligar — não copiar o corpus inteiro.\n",
  ].join("\n");
  writeFileSync(path, content, "utf8");
  refreshWikiIndex(m);
  return { id, path, wiki_size_warning: wikiTotalBytes(m) > WIKI_WARN_BYTES };
}

function wikiTotalBytes(m) {
  let n = 0;
  for (const f of readdirSync(m.wiki)) {
    if (!f.endsWith(".md")) continue;
    n += statSync(join(m.wiki, f)).size;
  }
  return n;
}

function refreshWikiIndex(m) {
  const entries = [];
  for (const f of readdirSync(m.wiki)) {
    if (!f.endsWith(".md") || f === "INDEX.md") continue;
    const text = readFileSync(join(m.wiki, f), "utf8");
    const title = text.match(/^# (.+)/m)?.[1] ?? f;
    const summary = text.split("\n\n")[1]?.split("\n")[0] ?? "";
    entries.push({ f, title, summary: summary.slice(0, 120) });
  }
  entries.sort((a, b) => a.title.localeCompare(b.title));
  const lines = [
    "# Wiki",
    "",
    ...entries.map((e) => `- **${e.title}** — ${e.summary} → [${e.f}](./${e.f})`),
    "",
    wikiTotalBytes(m) > WIKI_WARN_BYTES
      ? "\n⚠ Wiki maior que o recomendado; rode `wb dream` para consolidar/resumir.\n"
      : "",
  ];
  writeFileSync(m.wikiIndex, lines.join("\n"), "utf8");
}

export function readWikiPage(id) {
  const m = memoryPaths();
  const path = join(m.wiki, `${id}.md`);
  if (!existsSync(path)) return null;
  return { id, text: readFileSync(path, "utf8") };
}

export function wikiStats() {
  const m = memoryPaths();
  if (!existsSync(m.wiki)) return { pages: 0, bytes: 0 };
  return { pages: readdirSync(m.wiki).filter((f) => f.endsWith(".md") && f !== "INDEX.md").length, bytes: wikiTotalBytes(m) };
}
