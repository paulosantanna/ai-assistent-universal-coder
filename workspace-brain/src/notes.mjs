import { writeFileSync, readFileSync, existsSync, unlinkSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { createHash } from "node:crypto";
import { ensureMemoryLayout, memoryPaths } from "./memory-layers.mjs";

function slug(title) {
  const base = title
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 60);
  const hash = createHash("sha256").update(title).digest("hex").slice(0, 8);
  return `${base || "note"}-${hash}`;
}

/**
 * Nota preditiva: regra + evidência + armadilhas (evitar memória errada/confiante).
 */
export function upsertNote({ title, rule, evidence = [], pitfalls = [], supersedes = null }) {
  if (!title?.trim() || !rule?.trim()) throw new Error("title e rule são obrigatórios");
  if (!evidence.length) throw new Error("evidence[] obrigatório (ponteiro transcript, path, digest)");

  const m = ensureMemoryLayout();
  const id = slug(title);
  const path = join(m.notes, `${id}.md`);
  const created = existsSync(path) ? null : new Date().toISOString();
  const body = [
    `# ${title}`,
    "",
    `Updated: ${new Date().toISOString().slice(0, 10)}`,
    supersedes ? `Supersedes: ${supersedes}` : "",
    "",
    "## Regra (previsão)",
    rule.trim(),
    "",
    "## Evidência",
    ...evidence.map((e) => `- ${e}`),
    "",
    "## Armadilhas",
    pitfalls.length ? pitfalls.map((p) => `- ${p}`).join("\n") : "- (nenhuma registrada)",
    "",
    "## Não guardar",
    "- Estado reobservável no repo (versões em lockfile, árvore de ficheiros) salvo decisão explícita.",
    "",
  ]
    .filter(Boolean)
    .join("\n");

  writeFileSync(path, body, "utf8");
  refreshNotesIndex(m);
  return { id, path, created };
}

function refreshNotesIndex(m) {
  const entries = [];
  for (const f of readdirSync(m.notes)) {
    if (!f.endsWith(".md") || f === "INDEX.md") continue;
    const text = readFileSync(join(m.notes, f), "utf8");
    const title = text.match(/^# (.+)/m)?.[1] ?? f;
    entries.push({ f, title });
  }
  entries.sort((a, b) => a.title.localeCompare(b.title));
  const lines = [
    "# Notes index",
    "",
    "> Lista curta para bootstrap. Uma linha por nota.",
    "",
    ...entries.map((e) => `- [${e.title}](./${e.f})`),
    "",
  ];
  writeFileSync(m.notesIndex, lines.join("\n"), "utf8");
}

export function deleteNote(id) {
  const m = ensureMemoryLayout();
  const path = join(m.notes, `${id}.md`);
  if (existsSync(path)) unlinkSync(path);
  refreshNotesIndex(m);
  return { deleted: id };
}

export function readNote(id) {
  const m = memoryPaths();
  const path = join(m.notes, `${id}.md`);
  if (!existsSync(path)) return null;
  return { id, path, text: readFileSync(path, "utf8") };
}
